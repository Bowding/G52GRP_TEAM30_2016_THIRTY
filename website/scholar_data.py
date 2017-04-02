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

def breathFirstSearch(url, current_user_id):
	relatedScholars.append(url)
		
	threads = []
	
	#print parent node name
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	
	getDataFromProfile(soup, current_user_id)
				
	#first degree - scholars the input scholar has collaborated with
	for link in soup.find_all("a", {"class": "gsc_rsb_aa"}):		
		name = link.text.encode('ascii', 'ignore').decode('ascii')	
		link = "https://scholar.google.co.uk" + link.get('href')
		user_id = link.split("user=")[1].split("AAAAJ")[0]
		relatedScholars.append(link)

		t = threading.Thread(target = secondDegree, args = (link, user_id, ))
		threads.append(t)
	    
	for t in threads:
		t.setDaemon(True)
		t.start()
	for t in threads:
		t.join()

#second degree - scholars the first degree scholar has collaborated with		
def secondDegree(url, current_user_id):
	#print parent node name
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	
	getDataFromProfile(soup, current_user_id)

	for link in soup.find_all("a", {"class": "gsc_rsb_aa"}):
		link = "https://scholar.google.co.uk" + link.get('href')
		user_id = link.split("user=")[1].split("AAAAJ")[0]
		
		#check if link exists in first degree array and the second degree array
		if link not in relatedScholars:
			if link not in relatedScholars2ndDegree:		
				relatedScholars2ndDegree.append(link)

				r = requests.get(link)
				soup = BeautifulSoup(r.content, "html.parser")
				
				getDataFromProfile(soup, user_id)
					
def getDataFromProfile(soup, current_user_id):
	name_data = soup.find_all("div", {"id": "gsc_prf_in"})[0]
	currentName = name_data.text.encode('ascii', 'ignore').decode('ascii')
	
	institution = soup.find_all("div", {"class": "gsc_prf_il"})[0]
	institutionName = institution.text.encode('ascii', 'ignore').decode('ascii')
	
	insertDB_institution(current_user_id, institutionName)
	
	for fields in soup.find_all("a", {"class": "gsc_prf_ila"}): 
		fieldName = fields.text.encode('ascii', 'ignore').decode('ascii')
		insertDB_fields(current_user_id, fieldName)
	
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
def insertDB_institution(user_id, institution):	
	#name = name.replace("'", ":")
	institution = institution.replace("'", ":")
	
	try:
		lock.acquire()
		f_sd.write("INSERT into institutions (scholarID, institution) VALUES ('%s','%s');" % (user_id, institution))
		lock.release()
	except ValueError:
		print("Failed inserting....")			
			
#insert scholar and institutionName into db			
def insertDB_fields(user_id, field):	
	try:
		lock.acquire()
		f_sd.write("INSERT into fields (scholarID, field) VALUES ('%s','%s');" % (user_id, field.replace("'", ":")))
		lock.release()
	except ValueError:
		print("Failed inserting....")			
			
if __name__ == "__main__":

	print("it's scholar_data.py!!!!!")
	
	f_sd = open('scholar_data.txt', 'w', encoding = 'utf-8')

	target_user_id = sys.argv[1]

	url = "https://scholar.google.co.uk/citations?user=" + target_user_id + "AAAAJ"
	
	breathFirstSearch(url, target_user_id)

	f_sd.close()
	print("finish scholar data")