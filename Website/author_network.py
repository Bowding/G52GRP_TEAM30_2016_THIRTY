import codecs
import requests
import pymysql
import sys
import os
from bs4 import BeautifulSoup
import threading
#import bottle_index

#urls
relatedScholars = []
relatedScholars2ndDegree = []

global f_an
global lock

lock = threading.Lock()
		
#A breadth first search pattern has been implemented to find unique scholars who are related to the input scholar

def breathFirstSearch(url, current_user_id):
	#print parent node name

	soup = perform_request(url)
	name_data = soup.find_all("div", {"id": "gsc_prf_in"})[0]
	currentName = name_data.text.encode('ascii', 'ignore').decode('ascii')
	threads = []

	print(currentName)
	#cur = conn.cursor()
	
	try:
		lock.acquire()
		f_an.write("INSERT into nodes (scholarID) VALUES ('%s');" % (current_user_id))
		lock.release()
		#conn.commit()
	except ValueError:
		print("Failed inserting....")	
	

	#url = soup.find_all("a", {"class": "gsc_rsb_lc"})[0]
	link = "https://scholar.google.co.uk/citations?view_op=list_colleagues&user=" + current_user_id
	
	#r = requests.get(link)
	#soup = BeautifulSoup(r.content, "html.parser")
	soup = perform_request(link)
		
	#first degree - scholars the input scholar has collaborated with
	for scholar in soup.findAll("div", {"class": "gsc_1usr_text"}):
#		name = link.text.encode('ascii', 'ignore').decode('ascii')
#		print(currentName + " " + name)

		scholarLink = scholar.find('a', href=True)

		user_id = scholarLink['href'].split("user=")[1].split("&")[0]
		link = "https://scholar.google.co.uk/citations?user=" + user_id

		#insert name of scholar and current node scholar into db
		try:
			lock.acquire()
			f_an.write("INSERT into connections (sourceScholarID, targetScholarID) VALUES ('%s','%s');" % (current_user_id, user_id))
			lock.release()
			#conn.commit()
		except ValueError:
			print("Failed inserting....")	
			
		#relatedScholars.append(link)

		t = threading.Thread(target = secondDegree, args = (link, user_id, ))
		threads.append(t)
	    
	for t in threads:
		t.setDaemon(True)
		t.start()
	for t in threads:
		t.join()

#second degree - scholars the first degree scholar has collaborated with		
def secondDegree(url, current_user_id):
	#r = requests.get(url)
	#soup = BeautifulSoup(r.content, "html.parser")
	soup = perform_request(url)
	
	#print parent node name
	#r = requests.get(url)
	#soup = BeautifulSoup(r.content, "html.parser")
	name_data = soup.find_all("div", {"id": "gsc_prf_in"})[0]
	currentName = name_data.text.encode('ascii', 'ignore').decode('ascii')

	print(currentName)

	try:
		lock.acquire()
		f_an.write("INSERT into nodes (scholarID) VALUES ('%s');" % (current_user_id))
		lock.release()
		#conn.commit()
	except ValueError:
		print("Failed inserting....")
		
	#r = requests.get(url)
	#soup = BeautifulSoup(r.content, "html.parser")

	#url = soup.find_all("a", {"class": "gsc_rsb_lc"})[0]
	link = "https://scholar.google.co.uk/citations?view_op=list_colleagues&user=" + current_user_id
	
	#r = requests.get(link)
	#soup = BeautifulSoup(r.content, "html.parser")
	soup = perform_request(link)
		
	for scholar in soup.findAll("div", {"class": "gsc_1usr_text"}):
		#print name 
#		name = link.text.encode('ascii', 'ignore').decode('ascii')
#		print(currentName + " " + name)
		
		scholarLink = scholar.find('a', href=True)
		user_id = scholarLink['href'].split("user=")[1].split("&")[0]
		link = "https://scholar.google.co.uk/citations?user=" + user_id

		#insert name of scholar and current node scholar into db
		try:
			lock.acquire()
			f_an.write("INSERT into connections (sourceScholarID, targetScholarID) VALUES ('%s','%s');" % (current_user_id, user_id))
			lock.release()
			#conn.commit()
		except ValueError:
			print("Failed inserting....")	
			

		#check if link exists in first degree array and the second degree array
		if link not in relatedScholars:
			if link not in relatedScholars2ndDegree:
				relatedScholars2ndDegree.append(link)
		

def perform_request(url):

	filename = "requestsCache/" + url.split("citations?")[1].replace(":","---")+ ".html"

	try:
		soup = BeautifulSoup(open(filename, encoding = 'utf-8'), "html.parser")
	except FileNotFoundError:
		r = requests.get(url)

		captchaContent = "Our systems have detected unusual traffic from your computer network."
		if captchaContent in r.text:
			print("could not connect to Google...")
			print(url)
			os._exit(1)
		else:
			f_r = open(filename, 'w', encoding = 'utf-8')
			f_r.write(r.text)
			f_r.close()

			soup = BeautifulSoup(r.content, "html.parser")

	return soup
							
if __name__ == "__main__":

	print("it's author_network.py!!!!!")
	
	#try:
	#	print("Connecting to mySQL.....")
	#	conn = pymysql.connect(host='localhost', db='googlescholardb', user='root', password='', cursorclass=pymysql.cursors.DictCursor)
	#	print("Connection established!")
	#except:
	#	print("Connection Failed!")
	
	if sys.version_info[0] < 3:
		f_an = codecs.open('author_network.txt', 'w', encoding = 'utf-8')
	else: 
		f_an = open('author_network.txt', 'w', encoding = 'utf-8')

	target_user_id = sys.argv[1]
	#target_user_id = "41m5j04AAAAJ"

	url = "https://scholar.google.co.uk/citations?user=" + target_user_id

	#perform_request(url)
	#print(url)
	#url = "https://scholar.google.co.uk/citations?user=qc6CJjYAAAAJ"
	breathFirstSearch(url, target_user_id)

	f_an.close()
	print("finish coauthor")
	
	#conn.close()