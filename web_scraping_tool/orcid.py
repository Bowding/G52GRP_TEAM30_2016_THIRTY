#Basic scraping for Orcid to show extendability 

import requests
import re
from bs4 import BeautifulSoup
import os
import time
global url
global r
global soup 

#profile	
def getProfile():
	orcidID = soup.find_all("span", {"class": "orcid-id"})[0]
	name = soup.find_all("h2", {"class": "full-name"})[0]
	for tag in soupp.find_all('span', {"class": "ng-binding"}):
		print(tag.text)
	#institution = (soup.find_all('span')).find_all('ng-binding')
	studyField = soup.find_all("span", {"name": "keyword"})[0]
	country = soup.find_all("span", {"name": "country"})[0]
	print("Orcid ID: " + orcidID.text + "\n")
	print("Author Name: " + ' '.join(name.text.split()))
	#print("Institution: " + institution.text)
	print("Field of Study: " + studyField.text)
	print("Country of Study: " + country.text)
                
    
if __name__ == "__main__":
	
	url = "http://orcid.org/0000-0002-8847-1856"
	r = requests.get(url)
	soupp = BeautifulSoup(r.content, 'lxml')
	soup = BeautifulSoup(r.content, "html.parser")
	getProfile()