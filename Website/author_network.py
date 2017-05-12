import codecs
import requests
import pymysql
import sys
import os
from bs4 import BeautifulSoup
import threading

#urls
relatedScholars = []
relatedScholars2ndDegree = []

global f_an
global lock

#create lock
lock = threading.Lock()
		
#A breadth first search pattern has been implemented to find unique scholars who are related to the input scholar
def breathFirstSearch(url, current_user_id):

	#try to perform a request to local cache or google if cache missed
	soup = perform_request(url)

	#get name of current scholar
	name_data = soup.find_all("div", {"id": "gsc_prf_in"})[0]
	currentName = name_data.text.encode('ascii', 'ignore').decode('ascii')
	threads = []

	print(currentName)
	
	#write parent node to db
	try:
		lock.acquire()
		f_an.write("INSERT into nodes (scholarID) VALUES ('%s');" % (current_user_id))
		lock.release()

	except ValueError:
		print("Failed inserting....")	
	

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

		#insert name of scholar and current node scholar into db
		try:
			lock.acquire()
			f_an.write("INSERT into connections (sourceScholarID, targetScholarID) VALUES ('%s','%s');" % (current_user_id, user_id))
			lock.release()

		except ValueError:
			print("Failed inserting....")

		#create a thread to get their coauthors for each coauthor in this degree
		t = threading.Thread(target = secondDegree, args = (link, user_id, ))
		threads.append(t)
	
	#actuate all threads   
	for t in threads:
		t.setDaemon(True)
		t.start()
	for t in threads:
		t.join()

#second degree - scholars the first degree scholar has collaborated with		
def secondDegree(url, current_user_id):

	#try to perform a request to local cache or google if cache missed
	soup = perform_request(url)
	
	#get name of current scholar
	name_data = soup.find_all("div", {"id": "gsc_prf_in"})[0]
	currentName = name_data.text.encode('ascii', 'ignore').decode('ascii')

	print(currentName)

	#write parent node to db
	try:
		lock.acquire()
		f_an.write("INSERT into nodes (scholarID) VALUES ('%s');" % (current_user_id))
		lock.release()
		#conn.commit()
	except ValueError:
		print("Failed inserting....")
	
	#generate link for coauthor google page for target scholar
	link = "https://scholar.google.co.uk/citations?view_op=list_colleagues&user=" + current_user_id
	
	#try to perform a request to local cache or google if cache missed
	soup = perform_request(link)
	
	#second degree - scholars the current scholar has collaborated with
	for scholar in soup.findAll("div", {"class": "gsc_1usr_text"}):
		
		#generating the user IDs and profile page url for first degree coauthors
		scholarLink = scholar.find('a', href=True)
		user_id = scholarLink['href'].split("user=")[1].split("&")[0]
		link = "https://scholar.google.co.uk/citations?user=" + user_id

		#insert name of scholar and current node scholar into db
		try:
			lock.acquire()
			f_an.write("INSERT into connections (sourceScholarID, targetScholarID) VALUES ('%s','%s');" % (current_user_id, user_id))
			lock.release()

		except ValueError:
			print("Failed inserting....")	

		#check if link exists in first degree array and the second degree array
		if link not in relatedScholars:
			if link not in relatedScholars2ndDegree:
				relatedScholars2ndDegree.append(link)
	

#try to perform a request to local cache or google if cache missed
def perform_request(url):

	#generate a filename from given url
	filename = "requestsCache/" + url.split("citations?")[1].replace(":","---")+ ".html"

	#try cache
	try:
                #to make the script compatible with python 2.7
                if sys.version_info[0] < 3:
                        soup = BeautifulSoup(codecs.open(filename, encoding = 'utf-8'), "html.parser")
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

	print("it's author_network.py!!!!!")
	
	#to make the script compatible with python 2.7 
	if sys.version_info[0] < 3:
		f_an = codecs.open('author_network.txt', 'w', encoding = 'utf-8')
	else: 
		f_an = open('author_network.txt', 'w', encoding = 'utf-8')

	#get argument as target_user_id
	target_user_id = sys.argv[1]

	#generate profile url
	url = "https://scholar.google.co.uk/citations?user=" + target_user_id

	#perform search
	breathFirstSearch(url, target_user_id)

	#close file
	f_an.close()
	print("finish coauthor")
	
	#conn.close()
