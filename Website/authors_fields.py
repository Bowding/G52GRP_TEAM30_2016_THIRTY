import requests
import pymysql
import sys
from bs4 import BeautifulSoup
import threading

#urls
relatedScholars = []
relatedScholars2ndDegree = []
global f_af
global lock

lock = threading.Lock()
		
#A breadth first search pattern has been implemented to find unique scholars who are related to the input scholar

def breathFirstSearch(url):
	relatedScholars.append(url)
	
	#print parent node name
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	
	name_data = soup.find_all("div", {"id": "gsc_prf_in"})[0]
	currentName = name_data.text.encode('ascii', 'ignore').decode('ascii')

	threads = []
	
	#cur = conn.cursor()
	
	for fields in soup.find_all("a", {"class": "gsc_prf_ila"}): 
		fieldName = fields.text.encode('ascii', 'ignore').decode('ascii')
		#print(currentName + " " + fieldName)
		#insertDB(currentName, fieldName)
		try:
			lock.acquire()
			f_af.write("INSERT into fields (scholarName, field) VALUES ('%s','%s');" % (currentName.replace("'", ":"), fieldName.replace("'", ":")))
			lock.release()
			#conn.commit()
		except ValueError:
			print("1111Failed inserting....")
		
	#first degree - scholars the input scholar has collaborated with
	for link in soup.find_all("a", {"class": "gsc_rsb_aa"}):		
		name = link.text.encode('ascii', 'ignore').decode('ascii')	
		link = "https://scholar.google.co.uk" + link.get('href')
		#relatedScholars.append(link)

		t = threading.Thread(target = secondDegree, args = (link, ))
		threads.append(t)
	    

	for t in threads:
		t.setDaemon(True)
		t.start()
	for t in threads:
		t.join()
		
	#for link1stDegree in relatedScholars:
	#	secondDegree(link1stDegree)
		
	#cur.close()

#second degree - scholars the first degree scholar has collaborated with		
def secondDegree(url):
	#print parent node name
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	
	name_data = soup.find_all("div", {"id": "gsc_prf_in"})[0]
	currentName = name_data.text.encode('ascii', 'ignore').decode('ascii')
	
	for fields in soup.find_all("a", {"class": "gsc_prf_ila"}): 
		fieldName = fields.text.encode('ascii', 'ignore').decode('ascii')	
		#print(currentName + " " + fieldName)
		#insertDB(currentName, fieldName)
		try:
			lock.acquire()
			f_af.write("INSERT into fields (scholarName, field) VALUES ('%s','%s');" % (currentName.replace("'", ":"), fieldName.replace("'", ":")))
			lock.release()
			#conn.commit()
		except ValueError:
			print("22222Failed inserting....")
		
	for link in soup.find_all("a", {"class": "gsc_rsb_aa"}):
		link = "https://scholar.google.co.uk" + link.get('href')
		
		#check if link exists in first degree array and the second degree array
		if link not in relatedScholars:
			if link not in relatedScholars2ndDegree:		
				relatedScholars2ndDegree.append(link)

				r = requests.get(link)
				soup = BeautifulSoup(r.content, "html.parser")
				
				name_data = soup.find_all("div", {"id": "gsc_prf_in"})[0]
				currentName = name_data.text.encode('ascii', 'ignore').decode('ascii')
				
				for fields in soup.find_all("a", {"class": "gsc_prf_ila"}): 
					fieldName = fields.text.encode('ascii', 'ignore').decode('ascii')	
					#print(currentName + " " + fieldName)
					#insertDB(currentName, fieldName)
		try:
			lock.acquire()
			f_af.write("INSERT into fields (scholarName, field) VALUES ('%s','%s');" % (currentName.replace("'", ":"), fieldName.replace("'", ":")))
			lock.release()
			#conn.commit()
		except ValueError:
			print("222222Failed inserting....")
				
#insert scholar and institutionName into db			
def insertDB(name, field):	
	name = name.replace("'", ":")
	field = field.replace("'", ":")
	
	try:
		f_af.write("INSERT into fields (scholarName, field) VALUES ('%s','%s');" % (name, field))
		#conn.commit()
	except ValueError:
		print("Failed inserting....")			
			


if __name__ == "__main__":

	print("it's authors_fields.py!!!!!")

	f_af = open('authors_fields.txt', 'w')

	url = "https://scholar.google.co.uk/citations?user=" + sys.argv[1]

	#url = "https://scholar.google.co.uk/citations?user=G0yAJAwAAAAJ&hl=en&oi=ao&cstart=0&pagesize=200"
	
	#try:
	#	print("Connecting to mySQL.....")
	#	conn = pymysql.connect(host='localhost', db='googlescholardb', user='root', password='', cursorclass=pymysql.cursors.DictCursor)
	#	print("Connection established!")
	#except:
	#	print("Connection Failed!")
	
	breathFirstSearch(url)
	f_af.close()
	print("finish author fields")
	
	#conn.close()