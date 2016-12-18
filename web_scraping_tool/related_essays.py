import requests
from bs4 import BeautifulSoup

relatedScholars = []
relatedScholars2ndDegree = []
relatedScholars3rdDegree = []

relatedScholars1stDegreeNames = []
relatedScholars2ndDegreeNames = []
relatedScholars2ndDegree1stDegreeCollaborations = []
relatedScholars3rdDegreeNames = []

publications = []
citations = []
		
#Gives the top 10 most cited papers in the input scholar's network
		
def breathFirstSearch(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")

	#first degree - scholars the input scholar has collaborated with
	for link in soup.find_all("a", {"class": "gsc_rsb_aa"}):
		link = "https://scholar.google.co.uk" + link.get('href')
		relatedScholars.append(link)
		getInformation(link, 1)
		
	print("Finished first degree")
		
	for link1stDegree in relatedScholars:
		getInformation(link1stDegree, 11)
		secondDegree(link1stDegree)

	print("Finished second degree")	
	
	x = 0
	for link2ndDegree in relatedScholars2ndDegree:
		getInformation(link2ndDegree, 12)
		secondDegreeScholar = relatedScholars2ndDegree1stDegreeCollaborations[x]
		thirdDegree(link2ndDegree)
		x += 1
		
	print("Finished third degree")

#second degree - scholars the first degree scholar has collaborated with		
def secondDegree(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	
	#limit to 3 for now
	x = 0
	for link in soup.find_all("a", {"class": "gsc_rsb_aa"}):
		if x == 3:
			break
	
		link = "https://scholar.google.co.uk" + link.get('href')
		
		#check if link exists in first degree array and the second degree array
		if link not in relatedScholars:
			if link not in relatedScholars2ndDegree:
				relatedScholars2ndDegree.append(link)
				getInformation(link, 2)
				relatedScholars2ndDegree1stDegreeCollaborations.append(firstDegreeScholar)
				x += 1
		
#third degree - scholars the second degree scholar has collaborated with				
def thirdDegree(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
		
	#limit to 3 for now
	y = 0
	for link in soup.find_all("a", {"class": "gsc_rsb_aa"}):
		if y == 3:
			break
	
		link = "https://scholar.google.co.uk" + link.get('href')
		
		#check if link exists in first, second and third degree arrays 
		if link not in relatedScholars:
			if link not in relatedScholars2ndDegree:
				if link not in relatedScholars3rdDegree: 
					relatedScholars3rdDegree.append(link)
					getInformation(link, 3)
					y += 1
		
def getInformation(url, degree):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	name_data = soup.find_all("div", {"id": "gsc_prf_in"})[0]
	
	currentName = name_data.text.encode('ascii', 'ignore').decode('ascii')

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
	
	article = soup.find_all("tr", {"class": "gsc_a_tr"})
	x = 1
	for item in article:
		if x == 11:		#get 10 papers only from scholar - temporary
			break		
			
		try:	
			if " " not in item.find_all("td", {"class": "gsc_a_c"})[0].text:		
				publications.append(item.find_all("a", {"class": "gsc_a_at"})[0].text.encode('ascii', 'ignore').decode('ascii'))
				citationsNumber = only_numerics(item.find_all("td", {"class": "gsc_a_c"})[0].text)
				citations.append(int(citationsNumber))
			x += 1	
		except ValueError:
			citations.append(int(0))
			break
		
def only_numerics(seq):
    seq_type= type(seq)
    return seq_type().join(filter(seq_type.isdigit, seq))
		
def findMostCitedEssay():
	h = len(publications)		
	Matrix = []
	
	for index in range(0, (h-1)):
		Matrix.append([citations[index], publications[index]])
				
	for index in range(1, (h-1)):
		currentValue = int(Matrix[index][0])
		tmpString = Matrix[index][1]
		position = index
		
		while position > 0 and Matrix[position-1][0] > currentValue:
			Matrix[position][0] = Matrix[position-1][0]
			Matrix[position][1] = Matrix[position-1][1]
			position = position-1
			
		Matrix[position][0] = currentValue
		Matrix[position][1] = tmpString
		
	for index in range(0, (h-1)):
		print(Matrix[index][0])
		print(Matrix[index][1])

if __name__ == "__main__":
	url = "https://scholar.google.co.uk/citations?user=G0yAJAwAAAAJ&hl=en&oi=ao&cstart=0&pagesize=200"
	getInformation(url, 0)
	breathFirstSearch(url)
	findMostCitedEssay()