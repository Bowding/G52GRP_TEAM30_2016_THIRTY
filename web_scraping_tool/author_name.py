import requests
from bs4 import BeautifulSoup
import os
from urllib.request import urlopen
import time

global url
global r
global soup 

#getAvatar
def getAvatar():

	avatarSrcset = soup.find_all("img", {"id": "gsc_prf_pup"})[0].get('srcset').split(',', 1)
	avatarURL_S = avatarSrcset[0]
	avatarURL_M = avatarSrcset[1]
	print("avatarURL_S: " + avatarURL_S)
	print("avatarURL_M: " + avatarURL_M)

#getCitationIndecies
def getCitationIndices():

	citationsIndices = soup.find_all("td", {"class": "gsc_rsb_std"})
	citations_all = citationsIndices[0]
	citations_since = citationsIndices[1]
	hIndex_all = citationsIndices[2]
	hIndex_since = citationsIndices[3]
	i10Index_all = citationsIndices[4]
	i10Index_since = citationsIndices[5]

	print("Citation indices\tAll\tSince2011")
	print("Citations\t\t" + citations_all.text + "\t" + citations_since.text)
	print("h-index\t\t\t" + hIndex_all.text + "\t" + hIndex_since.text)
	print("i10Index\t\t" + i10Index_all.text + "\t" + i10Index_since.text)

#profile	
def getProfile():
	
	name = soup.find_all("div", {"id": "gsc_prf_in"})[0]
	institution = soup.find_all("div", {"class": "gsc_prf_il"})[0]
	studyField = soup.find_all("div", {"class": "gsc_prf_il"})[1]

	print("Author Name: " + name.text)
	print("Institution: " + institution.text)
	print("studyField: " + studyField.text)

	getAvatar();
	getCitationIndices();

def getCoCoAuthors(href):

	link = "https://scholar.google.co.uk" + href
	coAu_r = requests.get(link)
	coAu_soup = BeautifulSoup(coAu_r.content, "html.parser")

	coCoAuthors = coAu_soup.find_all("a", {"class": "gsc_rsb_aa"})
	print("\tCo-Authors:")
	for item in coCoAuthors:
		print("\t" + item.text.encode('ascii', 'ignore').decode('ascii'))


#co-authors
def getCoAuthors():

	coAuthors = soup.find_all("a", {"class": "gsc_rsb_aa"})
	print("Co-Authors:")
	for item in coAuthors:
		coAuthors_href = item.get('href')	#get a list of link to coAuthor profiles
		print(item.text.encode('ascii', 'ignore').decode('ascii') + "\t" + coAuthors_href)
		getCoCoAuthors(coAuthors_href)

#get top-5 cited article
def getTop5CitedArticle():

	nextArtBlock = soup.find("tr", {"class": "gsc_a_tr"})
	nextCitedNum = nextArtBlock.find("a", {"class": "gsc_a_ac"})
	nextArt = nextArtBlock.find("a", {"class": "gsc_a_at"})

	print("\nTop-5 cited articles:")

	for i in range(5):

		if nextCitedNum == "&nbsp":
			break
		else:
			print("NO.%d "% (i + 1) + nextArt.text + " (Cited by: " + nextCitedNum.text + ")")
			preCitedNum = nextCitedNum
			nextArtBlock = nextArtBlock.find_next_sibling("tr", {"class": "gsc_a_tr"})
			if nextArtBlock == None:
				break	#same citation number next page??????
			nextCitedNum = nextArtBlock.find("a", {"class": "gsc_a_ac"})
			nextArt = nextArtBlock.find("a", {"class": "gsc_a_at"})
			i += 1

		if i == 5:	#if is last iteration, check next
			j = i
			while(nextCitedNum.text == preCitedNum.text):	#if next have same citation number, print and check next
				
				print("NO.%d "% (j+1) + nextArt.text + " (Cited by: " + nextCitedNum.text + ")")
				preCitedNum = nextCitedNum
				nextArtBlock = nextArtBlock.find_next_sibling("tr", {"class": "gsc_a_tr"})
				if nextArtBlock == None:
					break	#same citation number next page???????
				nextCitedNum = nextArtBlock.find("a", {"class": "gsc_a_ac"})
				nextArt = nextArtBlock.find("a", {"class": "gsc_a_at"})

				j += 1



#authors cited him
#def citationAuthors():

#cited authors
#def citedAuthors():

#main		
if __name__ == "__main__":
	
	url = "https://scholar.google.co.uk/citations?user=33ftCdEAAAAJ&hl=en"
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")

	getProfile()
	getCoAuthors()
	getTop5CitedArticle()