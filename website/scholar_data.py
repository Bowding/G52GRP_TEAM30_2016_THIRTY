import requests
import pymysql
import sys
from bs4 import BeautifulSoup
import threading

#urls
relatedScholars = []
relatedScholars2ndDegree = []

global f_sd
global lock

lock = threading.Lock()
	
#A breadth first search pattern has been implemented to find unique scholars who are related to the input scholar

def breathFirstSearch(url):
	relatedScholars.append(url)
		
	threads = []
	
	#print parent node name
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	
	getDataFromProfile(soup, url)
				
	#first degree - scholars the input scholar has collaborated with
	for link in soup.find_all("a", {"class": "gsc_rsb_aa"}):		
		name = link.text.encode('ascii', 'ignore').decode('ascii')	
		link = "https://scholar.google.co.uk" + link.get('href')
		relatedScholars.append(link)

		t = threading.Thread(target = secondDegree, args = (link, ))
		threads.append(t)
	    
	for t in threads:
		t.setDaemon(True)
		t.start()
	for t in threads:
		t.join()

#second degree - scholars the first degree scholar has collaborated with		
def secondDegree(url):
	#print parent node name
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	
	getDataFromProfile(soup, url)

	for link in soup.find_all("a", {"class": "gsc_rsb_aa"}):
		link = "https://scholar.google.co.uk" + link.get('href')
		
		#check if link exists in first degree array and the second degree array
		if link not in relatedScholars:
			if link not in relatedScholars2ndDegree:		
				relatedScholars2ndDegree.append(link)

				r = requests.get(link)
				soup = BeautifulSoup(r.content, "html.parser")
				
				getDataFromProfile(soup, link)
					
def getDataFromProfile(soup, url):
	name_data = soup.find_all("div", {"id": "gsc_prf_in"})[0]
	currentName = name_data.text.encode('ascii', 'ignore').decode('ascii')
	currentURL = url
	
	institution = soup.find_all("div", {"class": "gsc_prf_il"})[0]
	institutionName = institution.text.encode('ascii', 'ignore').decode('ascii')
	
	insertDB_institution(currentURL, institutionName)
	
	for fields in soup.find_all("a", {"class": "gsc_prf_ila"}): 
		fieldName = fields.text.encode('ascii', 'ignore').decode('ascii')
		insertDB_fields(currentURL, fieldName)
	
	#for every paper listed on profile, get the paper title and author name
	for paper in soup.find_all("tr", {"class": "gsc_a_tr"}):	
		paperTitle = paper.text.encode('ascii', 'ignore').decode('ascii')
		
		author_data = paper.find_all("div", {"class": "gs_gray"})[0]
		authors = author_data.text.encode('ascii', 'ignore').decode('ascii')
		
		insertDB_paperData(paperTitle, authors)				
							
#insert paper and and paper co-authors into db			
def insertDB_paperData(paper, authors):	
	paper = paper.replace("'", ":")
	authors = authors.replace("'", ":")
	
	try:
		lock.acquire()
		f_sd.write("INSERT into paperCoAuthors (paperTitle, paperAuthors) VALUES ('%s','%s');" % (paper, authors))
		lock.release()
	except ValueError:
		print("Failed inserting....")			
			
#insert scholar and institutionName into db			
def insertDB_institution(url, institution):	
	#name = name.replace("'", ":")
	institution = institution.replace("'", ":")
	
	try:
		lock.acquire()
		f_sd.write("INSERT into institutions (scholarURL, institution) VALUES ('%s','%s');" % (url, institution))
		lock.release()
	except ValueError:
		print("Failed inserting....")			
			
#insert scholar and institutionName into db			
def insertDB_fields(url, field):	
	try:
		lock.acquire()
		f_sd.write("INSERT into fields (scholarURL, field) VALUES ('%s','%s');" % (url, field.replace("'", ":")))
		lock.release()
	except ValueError:
		print("Failed inserting....")			
			
if __name__ == "__main__":

	print("it's scholar_data.py!!!!!")
	
	f_sd = open('scholar_data.txt', 'w', encoding = 'utf-8')

	url = "https://scholar.google.co.uk/citations?user=" + sys.argv[1]
	
	breathFirstSearch(url)

	f_sd.close()
	print("finish scholar data")