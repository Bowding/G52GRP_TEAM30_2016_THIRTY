#-*-coding:utf-8-*-
import codecs
import requests
import pymysql
import sys
from bs4 import BeautifulSoup
import threading
import re
from author_network import perform_request

#to make the script compatible with python 2.7 
if sys.version_info[0] < 3:
	reload(sys)
	sys.setdefaultencoding('utf8') 

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
	#r = requests.get(url)
	#f = open('test.html', 'w', encoding = 'utf-8')
	#soup = BeautifulSoup(r.content, "html.parser")
	#soup = perform_request(url)
	#f.write(r.text)
	#f.close()
	getDataFromProfile(current_user_id)
	
	#r = requests.get(url)
	#soup = BeautifulSoup(r.content, "html.parser")

	#url = soup.find_all("a", {"class": "gsc_rsb_lc"})[0]
	link = "https://scholar.google.co.uk/citations?view_op=list_colleagues&user=" + current_user_id
	
	#r = requests.get(link)
	#soup = BeautifulSoup(r.content, "html.parser")
	soup = perform_request(link)
					
	#first degree - scholars the input scholar has collaborated with
	for scholar in soup.findAll("div", {"class": "gsc_1usr_text"}):
		scholarLink = scholar.find('a', href=True)
		#link = "https://scholar.google.co.uk" + scholarLink['href']
		#user_id = link.split("user=")[1].split("&")[0]
		user_id = scholarLink['href'].split("user=")[1].split("&")[0]
		link = "https://scholar.google.co.uk/citations?user=" + user_id
		
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
	#r = requests.get(url)
	#soup = BeautifulSoup(r.content, "html.parser")
	#soup = perform_request(url)
	
	getDataFromProfile(current_user_id)
	
	#r = requests.get(url)
	#soup = BeautifulSoup(r.content, "html.parser")

	#url = soup.find_all("a", {"class": "gsc_rsb_lc"})[0]
	link = "https://scholar.google.co.uk/citations?view_op=list_colleagues&user=" + current_user_id
	
	#r = requests.get(link)
	#soup = BeautifulSoup(r.content, "html.parser")
	soup = perform_request(link)
		
	for scholar in soup.findAll("div", {"class": "gsc_1usr_text"}):
		scholarLink = scholar.find('a', href=True)
		#link = "https://scholar.google.co.uk" + scholarLink['href']
		#user_id = link.split("user=")[1].split("&")[0]
		user_id = scholarLink['href'].split("user=")[1].split("&")[0]
		link = "https://scholar.google.co.uk/citations?user=" + user_id
		
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

	url = "https://scholar.google.co.uk/citations?user=" + current_user_id + "&oi=ao&cstart=0&pagesize=100"

	#r = requests.get(url)
	#soup = BeautifulSoup(r.content, "html.parser")
	soup = perform_request(url)

	name_data = soup.find_all("div", {"id": "gsc_prf_in"})[0]
	currentName = name_data.text
	
	institution = soup.find_all("div", {"class": "gsc_prf_il"})[0]
	institutionName = institution.text
	
	insertDB_institution(current_user_id, institutionName)

	nation_data = soup.find_all("div", {"id": "gsc_prf_ivh"})[0].text
	if ".uk" in nation_data:
		nation = "uk"
	else:
		nation = "non-uk"

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
			
			paperID = paper.find("td", {"class": "gsc_a_t"}).find("a", {"class": "gsc_a_at"}).get('href').split(":")[1]
			#getDataOfPaper(current_user_id, paperID)

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
		url = "https://scholar.google.co.uk/citations?user=" + current_user_id + "&oi=ao&cstart=%d&pagesize=100" % (cstart)

		#access to next page
		#r = requests.get(url)
		#soup = BeautifulSoup(r.content, "html.parser")
		soup = perform_request(url)
			
	insertDB_profileData(currentName, paperCount, hIndexValue, nation, current_user_id)
	#print(currentName + "+++ %d" % paperCount)	

def getDataOfPaper(current_user_id, paperID):
	paperURL = "https://scholar.google.co.uk/citations?view_op=view_citation&user=" + current_user_id + "&citation_for_view=" + current_user_id + ":" + paperID
	
	#paper_r = requests.get(paperURL)
	#paper_soup = BeautifulSoup(paper_r.content, "html.parser")
	paper_soup = perform_request(paperURL)

	#get paper title
	paperName = paper_soup.find_all("div", {"id": "gsc_title"})[0].text

	index = 0
	data = paper_soup.find_all("div", {"class": "gs_scl"})

	#get author names if exist
	if data[index].find("div", {"class": "gsc_field"}).text == "Authors":
		authorNames = data[index].find("div", {"class": "gsc_value"}).text
		index += 1
	else:
		authorNames = ""

	#get publication date if exists
	if data[index].find("div", {"class": "gsc_field"}).text == "Publication date":
		publicationDate = data[index].find("div", {"class": "gsc_value"}).text
	else:
		publicationDate = ""

	#get citation number if exists
	citationDataArea = paper_soup.findAll(text=re.compile("Cited by"), limit = 1)
	if len(citationDataArea) != 0:
		citationData = citationDataArea[0]
	else:
		citationData = "Cited by 0"

	#get description if exists
	descriptionArea = paper_soup.find_all("div", {"id": "gsc_descr"})
	if len(descriptionArea) != 0:
		description = descriptionArea[0].text
	else:
		description = ""

	insertDB_paperData(paperName, authorNames, publicationDate, citationData, description, paperID)

#insert paper and and paper co-authors into db			
def insertDB_profileData(name, numberOfPapers, hIndex, nation, user_id):	
	name = name.replace("'","\\\'")
	
	try:
		lock.acquire()
		f_sd.write("INSERT into profile (aName, NumPaper, hIndex, nation, authorID) VALUES ('%s','%s','%d','%s','%s');" % (name, numberOfPapers, hIndex, nation, user_id))
		lock.release()
	except ValueError:
		print("Failed inserting....")	

#insert paper and and paper co-authors into db			
def insertDB_paperData(paperName, authorNames, publicationDate, citationData, description, paperID):
	#print("=====" + authorNames)
	paperName = paperName.replace("'","\\\'")
	authorNames = authorNames.replace("'","\\\'")
	publicationYear = publicationDate.split("/")[0]
	description = description.replace("'","\\\'")
	numberOfCitations = citationData.split("Cited by ")[1]
	print(numberOfCitations)
	#sys.exit(1)

	if publicationYear != "":
		try:
			lock.acquire()
			f_sd.write("INSERT into papers (paperName, authorNames, publicationYear, numberOfCitations, description, paperID) VALUES ('%s', '%s', %d, %d, '%s', '%s');" % (paperName, authorNames, int(publicationYear), int(numberOfCitations), description, paperID))
			lock.release()
		except ValueError:
			print("Failed inserting....")
	else:
		try:
			lock.acquire()
			f_sd.write("INSERT into papers (paperName, authorNames, numberOfCitations, description, paperID) VALUES ('%s', '%s', %d, '%s', '%s');" % (paperName, authorNames, int(numberOfCitations), description, paperID))
			lock.release()
		except ValueError:
			print("Failed inserting....")
			
#insert scholar and institutionName into db			
def insertDB_institution(user_id, institution):	
	#name = name.replace("'", ":")
	institution = institution.replace("'","\\\'")
	
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
	
	if sys.version_info[0] < 3:
		f_sd = codecs.open('scholar_data.txt', 'w', encoding = 'utf-8')
	else: 
		f_sd = open('scholar_data.txt', 'w', encoding = 'utf-8')

	target_user_id = sys.argv[1]
	#target_user_id = "8maqKdgAAAAJ"

	url = "https://scholar.google.co.uk/citations?user=" + target_user_id + "&cstart=0&pagesize=100"
	
	breathFirstSearch(url, target_user_id)

	f_sd.close()
	print("finish scholar data")