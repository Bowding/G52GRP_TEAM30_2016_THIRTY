import requests
from bs4 import BeautifulSoup

relatedScholars = []
relatedScholars2ndDegree = []
relatedScholars3rdDegree = []

relatedScholars1stDegreeNames = []
relatedScholars2ndDegreeNames = []
relatedScholars2ndDegree1stDegreeCollaborations = []
relatedScholars3rdDegreeNames = []
		
#A breadth first search pattern has been implemented to find unique scholars who are related to the input scholar
		
def breathFirstSearch(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")

	#first degree - scholars the input scholar has collaborated with
	for link in soup.find_all("a", {"class": "gsc_rsb_aa"}):
		link = "https://scholar.google.co.uk" + link.get('href')
		relatedScholars.append(link)
		getInformation(link, 1)
		
	for link1stDegree in relatedScholars:
		getInformation(link1stDegree, 11)
		secondDegree(link1stDegree)

	x = 0
	for link2ndDegree in relatedScholars2ndDegree:
		getInformation(link2ndDegree, 12)
		secondDegreeScholar = relatedScholars2ndDegree1stDegreeCollaborations[x]
		thirdDegree(link2ndDegree)
		x += 1

#second degree - scholars the first degree scholar has collaborated with		
def secondDegree(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	
	for link in soup.find_all("a", {"class": "gsc_rsb_aa"}):
		link = "https://scholar.google.co.uk" + link.get('href')
		
		#check if link exists in first degree array and the second degree array
		if link not in relatedScholars:
			if link not in relatedScholars2ndDegree:
				relatedScholars2ndDegree.append(link)
				getInformation(link, 2)
				relatedScholars2ndDegree1stDegreeCollaborations.append(firstDegreeScholar)
		
#third degree - scholars the second degree scholar has collaborated with				
def thirdDegree(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	
	for link in soup.find_all("a", {"class": "gsc_rsb_aa"}):
		link = "https://scholar.google.co.uk" + link.get('href')
		
		#check if link exists in first, second and third degree arrays 
		if link not in relatedScholars:
			if link not in relatedScholars2ndDegree:
				if link not in relatedScholars3rdDegree: 
					relatedScholars3rdDegree.append(link)
					getInformation(link, 3)
		
def getInformation(url, degree):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	name_data = soup.find_all("div", {"id": "gsc_prf_in"})[0]
	
	#soup = BeautifulSoup(response.read().decode('utf-8', 'ignore'))

	currentName = name_data.text.encode('utf-8', 'ignore').decode('utf-8')
	
	if degree == 0:
		print("Author Name - Input Scholar Name: " + currentName)
		global inputScholar 
		inputScholar = currentName
	elif degree == 1:
		print("Author Name - First Degree: " + currentName + " Path: " + inputScholar)	
		relatedScholars1stDegreeNames.append(currentName)
	elif degree == 2:
		print("Author Name - Second Degree: " + currentName + " Path: " + inputScholar + " -> " + firstDegreeScholar)	
		relatedScholars2ndDegreeNames.append(currentName)
	elif degree == 3:
		print("Author Name - Third Degree: " + currentName + " Path: " + inputScholar + " -> " + firstDegreeScholar + " -> " + secondDegreeScholar)	
		relatedScholars3rdDegreeNames.append(currentName)
	elif degree == 11:
		global firstDegreeScholar
		firstDegreeScholar = currentName
	elif degree == 12: 
		global secondDegreeScholar
		secondDegreeScholar = currentName
				
if __name__ == "__main__":
	url = "https://scholar.google.co.uk/citations?user=G0yAJAwAAAAJ&hl=en&oi=ao&cstart=0&pagesize=200"
	getInformation(url, 0)
	breathFirstSearch(url)