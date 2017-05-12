#Basic scraping for Scopus to show extendability

import requests
import re
from bs4 import BeautifulSoup

#profile	
def getSearchResults():
    x = soup.find("h3", {"class": "gs_rt"})
    y = x.find("a")
    searchPage = "https://scholar.google.co.uk/" + y['href']

    req = requests.get(searchPage)
    searchSoup = BeautifulSoup(req.content, "html.parser")
    results = searchSoup.findAll("div", {"class": "gsc_1usr_text"})   
    for scholar in results:
     print (scholar.text)
     scholarLink = scholar.find('a', href=True)
     print(scholarLink['href'] + "\n")



if __name__ == "__main__":
	
	url = "https://scholar.google.co.uk/scholar?q=andrew+parkes"
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	getSearchResults()
	
