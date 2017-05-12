#-*-coding:utf-8-*-
import codecs
import requests
import pymysql
import sys
from bs4 import BeautifulSoup
import threading
import re

#to make the script compatible with python 2.7 
if sys.version_info[0] < 3:
	reload(sys)
	sys.setdefaultencoding('utf8') 

#urls
relatedScholars = []
relatedScholars2ndDegree = []

global f_sd
global lock

#create lock
lock = threading.Lock()
	
#A breadth first search pattern has been implemented to find unique scholars who are related to the input scholar
def breathFirstSearch(url, current_user_id):
	global inputURL
	inputURL = url
	
	threads = []

	#get profile data of target scholar
	getDataFromProfile(current_user_id)

	#generate link for coauthor google page for target scholar
	link = "https://scholar.google.co.uk/citations?view_op=list_colleagues&user=" + current_user_id

	#try to perform a request to local cache or google if cache missed
	soup = perform_request(link)
			
	#first degree - scholars the input scholar has collaborated with
	for scholar in soup.findAll("div", {"class": "gsc_1usr_text"}):

		#generating the user IDs and profile page url for first degree coauthors
		scholarLink = scholar.find('a', href=True)
		user_id = scholarLink['href'].split("user=")[1].split("&")[0]
		link = "https://scholar.google.co.uk/citations?user=" + user_id
		
		#check whether there is a duplication
		if link not in inputURL:
			relatedScholars.append(link)

		#create a thread to get their coauthors for each coauthor in this degree
		t = threading.Thread(target = secondDegree, args = (link, user_id, ))
		threads.append(t)

	#actuate all threads
	for t in threads:
		t.setDaemon(True)
		t.start()
	for t in threads:
		t.join()

	print("finish first degree: "+ current_user_id)


#second degree - scholars the first degree scholar has collaborated with		
def secondDegree(url, current_user_id):

	threads = []
	
	#get profile data of current scholar
	getDataFromProfile(current_user_id)

	#generate link for coauthor google page for current scholar
	link = "https://scholar.google.co.uk/citations?view_op=list_colleagues&user=" + current_user_id
	
	#try to perform a request to local cache or google if cache missed
	soup = perform_request(link)

	#second degree - scholars the current scholar has collaborated with
	for scholar in soup.findAll("div", {"class": "gsc_1usr_text"}):

		#generating the user IDs and profile page url for second degree coauthors
		scholarLink = scholar.find('a', href=True)
		user_id = scholarLink['href'].split("user=")[1].split("&")[0]
		link = "https://scholar.google.co.uk/citations?user=" + user_id
		
		#check if link exists in first degree array and the second degree array
		if link not in relatedScholars:
			if link not in relatedScholars2ndDegree:
				if link not in inputURL:
					relatedScholars2ndDegree.append(link)
					
					#create a thread to get their coauthors for each coauthor in this degree
					t = threading.Thread(target = getDataFromProfile, args = (user_id, ))
					threads.append(t)

	#actuate all threads
	for t in threads:
		t.setDaemon(True)
		t.start()
	for t in threads:
		t.join()

	print("finish second degree: "+ current_user_id)

#scrape data from a scholar profile page					
def getDataFromProfile(current_user_id):

	threads = []

	#generate a link of profile page containing 100 papers
	url = "https://scholar.google.co.uk/citations?user=" + current_user_id + "&oi=ao&cstart=0&pagesize=100"

	#try to perform a request to local cache or google if cache missed
	soup = perform_request(url)

	#get name of current scholar
	name_data = soup.find_all("div", {"id": "gsc_prf_in"})[0]
	currentName = name_data.text
	
	#get institution of current scholar
	institution = soup.find_all("div", {"class": "gsc_prf_il"})[0]
	institutionName = institution.text
	
	#insert institution info
	insertDB_institution(current_user_id, institutionName)

	#get nation of current scholar
	nation_data = soup.find_all("div", {"id": "gsc_prf_ivh"})[0].text

	#check whether it is in uk
	if ".uk" in nation_data:
		nation = "uk"
	else:
		nation = "non-uk"

	#get the field of study of current scholar and insert them seperately using threads
	for fields in soup.find_all("a", {"class": "gsc_prf_ila"}): 
		fieldName = fields.text
		t = threading.Thread(target = insertDB_fields, args = (current_user_id, fieldName, ))
		threads.append(t)

	for t in threads:
		t.setDaemon(True)
		t.start()
	for t in threads:
		t.join()

	#get citation and hindex of current scholar
	hIndex_citation = soup.find_all("td", {"class": "gsc_rsb_std"})
	citationNum = int(hIndex_citation[0].text)
	hIndexValue = int(hIndex_citation[2].text)

	#get url of image of current scholar
	avatarSrcset = soup.find_all("img", {"id": "gsc_prf_pup"})[0].get('srcset').split(',', 1)
	avatarURL_S = avatarSrcset[0].split(" ")[0]

	#for every paper listed on profile, get the paper title and author name
	paperCount = 1;
	cstart = 0
	while(1):
		for paper in soup.find_all("tr", {"class": "gsc_a_tr"}):
			
			#the following commented codes will make huge amount of requests to google, can be put into used when we decide to add this funtionality later
			#paperID = paper.find("td", {"class": "gsc_a_t"}).find("a", {"class": "gsc_a_at"}).get('href').split(":")[1]
			#getDataOfPaper(current_user_id, paperID)

			#increment paper number
			paperCount += 1;
		
		#increment paper start number
		cstart +=100

		#get this page paper number
		this_page_NumPaper_range = soup.find("span", {"id": "gsc_a_nn"})

		#check whether have any more paper
		if(this_page_NumPaper_range != None):
			this_page_NumPaper_range = this_page_NumPaper_range.text
			this_page_NumPaper = int(this_page_NumPaper_range.split('–')[1])

			#if there is no paper on the next page
			if(this_page_NumPaper < cstart):
				paperCount -= 1
				break
		#if there is no paper on the current page
		else:
			paperCount -= 2
			break
		
		#otherwise	
		#get next page url
		url = "https://scholar.google.co.uk/citations?user=" + current_user_id + "&oi=ao&cstart=%d&pagesize=100" % (cstart)

		#access to next page
		soup = perform_request(url)
	
	#insert profile data to db		
	insertDB_profileData(currentName, paperCount, hIndexValue, citationNum, nation, current_user_id, avatarURL_S)


#the following function will make huge amount of requests to google, can be put into used when we decide to add this funtionality later
#get relative data of a paper
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
def insertDB_profileData(name, numberOfPapers, hIndex, citationNum, nation, user_id, avatarURL_S):

	name = name.replace("'","\\\'")
	
	try:
		lock.acquire()
		f_sd.write("INSERT into profile (aName, NumPaper, hIndex, citationNum, nation, authorID, avatarURL_S) VALUES ('%s','%s','%d','%d','%s','%s','%s');" % (name, numberOfPapers, hIndex, citationNum, nation, user_id, avatarURL_S))
		lock.release()
	except ValueError:
		print("Failed inserting....")	


#insert paper and and paper co-authors into db			
def insertDB_paperData(paperName, authorNames, publicationDate, citationData, description, paperID):

	paperName = paperName.replace("'","\\\'")
	authorNames = authorNames.replace("'","\\\'")
	publicationYear = publicationDate.split("/")[0]
	description = description.replace("'","\\\'")
	numberOfCitations = citationData.split("Cited by ")[1]

	#check whether there is publication year for this paper
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

#try to perform a request to local cache or google if cache missed
def perform_request(url):

	#generate a filename from given url
	filename = "requestsCache/" + url.split("citations?")[1].replace(":","---")+ ".html"

	#try cache
	try:
                #to make the script compatible with python 2.7 
                if sys.version_info[0] < 3:
                        soup = BeautifulSoup(codecs.open(filename, encoding = 'utf-8'), "html.parser"
                else:                
                        soup = BeautifulSoup(open(filename, encoding = 'utf-8'), "html.parser")

	#cache miss, request to google
	except FileNotFoundError:
		r = requests.get(url)

		captchaContent = "Our systems have detected unusual traffic from your computer network."

		#check whether the requested page is redirected to CAPTCHA page
		if captchaContent in r.text:
			print("could not connect to Google...")
			print(url)
			os._exit(1)
		else:
                        #to make the script compatible with python 2.7 
                        if sys.version_info[0] < 3:
                                f_r = codecs.open(filename, 'w', encoding = 'utf-8')
                        else: 
                                f_r = open(filename, 'w', encoding = 'utf-8')
			
			f_r.write(r.text)
			f_r.close()

			soup = BeautifulSoup(r.content, "html.parser")

	return soup

			
if __name__ == "__main__":

	print("it's scholar_data.py!!!!!")
	
	#to make the script compatible with python 2.7 
	if sys.version_info[0] < 3:
		f_sd = codecs.open('scholar_data.txt', 'w', encoding = 'utf-8')
	else: 
		f_sd = open('scholar_data.txt', 'w', encoding = 'utf-8')

	#get argument as target_user_id
	target_user_id = sys.argv[1]

	#generate profile url
	url = "https://scholar.google.co.uk/citations?user=" + target_user_id + "&cstart=0&pagesize=100"
	
	#perform search
	breathFirstSearch(url, target_user_id)

	#close file
	f_sd.close()
	print("finish scholar data")
