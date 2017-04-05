#-*-coding:utf-8-*-
import codecs
import requests
import pymysql
import sys
from bs4 import BeautifulSoup
import threading

#following codes is only needed for python 2.x and only works for python 2.x
#reload(sys)
#sys.setdefaultencoding('utf8')

#urls
relatedScholars = []
relatedScholars2ndDegree = []

global f_sd
global lock
#global lock2

lock = threading.Lock()
#lock2 = threading.Lock()
	
#A breadth first search pattern has been implemented to find unique scholars who are related to the input scholar

def breathFirstSearch(url, current_user_id):
	global inputURL
	inputURL = url
	
	threads = []
	
	#print parent node name
	r = requests.get(url)
#	f = open('test.html', 'w', encoding = 'utf-8')
	soup = BeautifulSoup(r.content, "html.parser")
#	f.write(soup.text)
#	f.close()
	getDataFromProfile(current_user_id)
				
	#first degree - scholars the input scholar has collaborated with
	for link in soup.find_all("a", {"class": "gsc_rsb_aa"}):		
		name = link.text	
		link = "https://scholar.google.co.uk" + link.get('href') 
		user_id = link.split("user=")[1].split("AAAAJ")[0]
		
		if link not in inputURL:
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

	threads = []

	#print parent node name
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	
	getDataFromProfile(current_user_id)

	for link in soup.find_all("a", {"class": "gsc_rsb_aa"}):
		link = "https://scholar.google.co.uk" + link.get('href')
		user_id = link.split("user=")[1].split("AAAAJ")[0]
		
		#check if link exists in first degree array and the second degree array
		if link not in relatedScholars:
			if link not in relatedScholars2ndDegree:
				if link not in inputURL:
					relatedScholars2ndDegree.append(link)
					
					r = requests.get(link)
					soup = BeautifulSoup(r.content, "html.parser")
					
					t = threading.Thread(target = getDataFromProfile, args = (user_id, ))
					threads.append(t)
					#getDataFromProfile(user_id)

	for t in threads:
		t.setDaemon(True)
		t.start()
	for t in threads:
		t.join()
					
def getDataFromProfile(current_user_id):
	threads = []

	url = "https://scholar.google.co.uk/citations?user=" + current_user_id + "AAAAJ" + "&oi=ao&cstart=0&pagesize=100"

	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")

	name_data = soup.find_all("div", {"id": "gsc_prf_in"})[0]
	currentName = name_data.text
	
	institution = soup.find_all("div", {"class": "gsc_prf_il"})[0]
	institutionName = institution.text
	
	insertDB_institution(current_user_id, institutionName)
	
	for fields in soup.find_all("a", {"class": "gsc_prf_ila"}): 
		fieldName = fields.text
		t = threading.Thread(target = insertDB_fields, args = (current_user_id, fieldName, ))
		threads.append(t)

	for t in threads:
		t.setDaemon(True)
		t.start()
	for t in threads:
		t.join()

		#insertDB_fields(current_user_id, fieldName)
	
	hIndex = soup.find_all("td", {"class": "gsc_rsb_std"})
	hIndexValue = int(hIndex[2].text)
	
	#for every paper listed on profile, get the paper title and author name
	paperCount = 1;
	cstart = 0
	while(1):
		for paper in soup.find_all("tr", {"class": "gsc_a_tr"}):	
			paperTitle = paper.text
			#print(paperTitle)
			
			#author_data = paper.find_all("div", {"class": "gs_gray"})[0]
			#authors = author_data.text.encode('ascii', 'ignore').decode('ascii')
			
			paperCount += 1;
			#insertDB_paperData(paperTitle, authors)		
		
		cstart +=100
		#print("0######################### %d" % paperCount)
		#get this page paper number
		this_page_NumPaper_range = soup.find("span", {"id": "gsc_a_nn"})
		if(this_page_NumPaper_range != None):
			this_page_NumPaper_range = this_page_NumPaper_range.text
			this_page_NumPaper = int(this_page_NumPaper_range.split('–')[1])
			if(this_page_NumPaper < cstart):
				paperCount -= 1
				#print("1######################### %d" % paperCount)
				#sys.exit()
				break
		else:
			#print("2######################### %d" % paperCount)
			paperCount -= 2
			#print("3######################### %d" % paperCount)
			#sys.exit()
			break
			
		#get next page url
		url = "https://scholar.google.co.uk/citations?user=" + current_user_id + "AAAAJ" + "&oi=ao&cstart=%d&pagesize=100" % (cstart)

		#access to next page
		r = requests.get(url)
		soup = BeautifulSoup(r.content, "html.parser")
			
	insertDB_profileData(currentName, paperCount, hIndexValue, current_user_id)
	#print(currentName + "+++ %d" % paperCount)	
		
#insert paper and and paper co-authors into db			
def insertDB_profileData(name, numberOfPapers, hIndex, user_id):	
	name = name.replace("'", ":")
	
	try:
		lock.acquire()
		f_sd.write("INSERT into profile (aName, NumPaper, hIndex, authorID) VALUES ('%s','%s','%d','%s');" % (name, numberOfPapers, hIndex, user_id))
		lock.release()
	except ValueError:
		print("Failed inserting....")	

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
	#target_user_id = "8maqKdg"

	url = "https://scholar.google.co.uk/citations?user=" + target_user_id + "AAAAJ" + "&cstart=0&pagesize=100"
	
	breathFirstSearch(url, target_user_id)

	f_sd.close()
	print("finish scholar data")