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
	#hIndex = soup.find_all("td", {"class": "gsc_rsb_std"})
	#article = soup.find_all("tr", {"class": "gsc_a_tr"})

	print("Author Name: " + name.text)
	print("Institution: " + institution.text)
	print("studyField: " + studyField.text)
	#print("h-index (all time): " + hIndex[2].text)
	#print("h-index (Since 2011): " + hIndex[3].text + "\n")
	getAvatar();
	getCitationIndices();
#	x = 1

#	for item in article:
#		print("Paper %d: "%(x) + item.find_all("a", {"class": "gsc_a_at"})[0].text.encode('ascii', 'ignore').decode('ascii'))
#		print("Year: " + item.find_all("td", {"class": "gsc_a_y"})[0].text.encode('ascii', 'ignore').decode('ascii'))
#		if item.find_all("td", {"class": "gsc_a_c"})[0].text != " ":
#			print("Cited by: " + item.find_all("td", {"class": "gsc_a_c"})[0].text.encode('ascii', 'ignore').decode('ascii'))
#		else:
#			print("Cited by: 0\n")
#		print("Co-Authors: " + item.find_all("div", {"class" : "gs_gray"})[0].text.encode('ascii', 'ignore').decode('ascii') + "\n")
#		x += 1	
#		
#	for link in soup.find_all("a", {"class": "gsc_rsb_aa"}):
#		link = "https://scholar.google.co.uk" + link.get('href')
#		print(link)
#		#basicInformation(link) 

#co-authors
def getCoAuthors():
	coAuthors = soup.find_all("a", {"class": "gsc_rsb_aa"})
	print("Co-Authors:")
	for item in coAuthors:
		print(item.text.encode('ascii', 'ignore').decode('ascii') + "\n")

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