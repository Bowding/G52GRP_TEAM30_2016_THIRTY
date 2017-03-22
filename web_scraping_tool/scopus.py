#Basic scraping for Scopus to show extendability

import requests
import re
from bs4 import BeautifulSoup

#profile	
def getProfile():
	authorID = soup.find("div", {"class": "authId"})
	name = soup.find_all("h1")[0]
	location = soup.find("div", {"class": "authAffilcityCounty"})
	institution = location.text.split(",")[0]
	studyField = soup.find_all("div", {"id": "subjAreas"})[0]
	country = location.text.split(",")[3]
	print(authorID.text + "\n")
	print("Author Name: " + name.text.split("details")[1])
	print("Institution: " + ''.join(institution.splitlines()))
	print("Field of Study: " + ''.join(studyField.text.splitlines()))
	print("Country of Study: " + ''.join(country.splitlines()))

if __name__ == "__main__":
	
	url = "https://www.scopus.com/authid/detail.uri?authorId=26642967000"
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	getProfile()
	
