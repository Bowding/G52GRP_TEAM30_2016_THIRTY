import requests
import pymysql
from bs4 import BeautifulSoup

#urls
relatedScholars = []
relatedScholars2ndDegree = []
		
#A breadth first search pattern has been implemented to find unique scholars who are related to the input scholar

def breathFirstSearch(url, conn):
	relatedScholars.append(url)
	
	#print parent node name
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	
	name_data = soup.find_all("div", {"id": "gsc_prf_in"})[0]
	currentName = name_data.text.encode('ascii', 'ignore').decode('ascii')
	
	institution = soup.find_all("div", {"class": "gsc_prf_il"})[0]
	
	try:
		institution2 = institution.find_all("a")[0]
		institutionName = institution2.text.encode('ascii', 'ignore').decode('ascii')
	except IndexError:
		institutionName = "Unknown"
	
	print(currentName + " Institution: " + institutionName)
	
	cur = conn.cursor()
		
	#first degree - scholars the input scholar has collaborated with
	for link in soup.find_all("a", {"class": "gsc_rsb_aa"}):		
		name = link.text.encode('ascii', 'ignore').decode('ascii')	
		link = "https://scholar.google.co.uk" + link.get('href')
		relatedScholars.append(link)
		
	for link1stDegree in relatedScholars:
		secondDegree(link1stDegree, cur)
		
	cur.close()

#second degree - scholars the first degree scholar has collaborated with		
def secondDegree(url, cur):
	#print parent node name
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	
	name_data = soup.find_all("div", {"id": "gsc_prf_in"})[0]
	currentName = name_data.text.encode('ascii', 'ignore').decode('ascii')
	
	institution = soup.find_all("div", {"class": "gsc_prf_il"})[0]
	
	try:
		institution2 = institution.find_all("a")[0]
		institutionName = institution2.text.encode('ascii', 'ignore').decode('ascii')
	except IndexError:
		institutionName = "Unknown"
	
	print(currentName + " Institution: " + institutionName)
	insertDB(currentName, institutionName, cur)		
		
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
				
				institution = soup.find_all("div", {"class": "gsc_prf_il"})[0]
				
				try:
					institution2 = institution.find_all("a")[0]
					institutionName = institution2.text.encode('ascii', 'ignore').decode('ascii')
				except IndexError:
					institutionName = "Unknown"
				
				print(currentName + " Institution: " + institutionName)
				insertDB(currentName, institutionName, cur)		
				
#insert scholar and institutionName into db			
def insertDB(name, institution, cur):	
	name = name.replace("'", ":")
	institution = institution.replace("'", ":")
	
	try:
		cur.execute("INSERT into institutions (scholarName, institution) VALUES ('%s','%s')" % (name, institution))
		conn.commit()
	except ValueError:
		print("Failed inserting....")			
			
if __name__ == "__main__":
	url = "https://scholar.google.co.uk/citations?user=G0yAJAwAAAAJ&hl=en&oi=ao&cstart=0&pagesize=200"
	
	try:
		print("Connecting to mySQL.....")
		conn = pymysql.connect(host='localhost', db='googlescholardb', user='root', password='', cursorclass=pymysql.cursors.DictCursor)
		print("Connection established!")
	except:
		print("Connection Failed!")
	
	breathFirstSearch(url, conn)
	
	conn.close()