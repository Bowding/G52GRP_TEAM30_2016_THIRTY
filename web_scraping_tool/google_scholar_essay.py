import requests
import re
from bs4 import BeautifulSoup
	
def essayInformation(url):
	r = requests.get(url)

	soup = BeautifulSoup(r.content, "html.parser")

	essay_name = soup.find_all("div", {"id": "gsc_title"})[0]
	author_names = soup.find_all("div", {"class": "gsc_value"})[0]
	publication_date = soup.find_all("div", {"class": "gsc_value"})[1]
	citation_data = soup.findAll(text=re.compile("Cited by"), limit = 1)[0]
	description = soup.find_all("div", {"id": "gsc_descr"})[0].text.encode('ascii', 'ignore').decode('ascii')
	


	print("\nEssay Title: " + essay_name.text)		
	print("Author(s): " + author_names.text)	
	print("Publication Date: " + publication_date.text)	
	print("Description: " + description)
	print(citation_data)
	
	for link in soup.find_all('a', href=True, text=citation_data, limit = 1):
		url2 = link['href']
	
	r = requests.get(url2)

	soup = BeautifulSoup(r.content, "html.parser")
	
	article = soup.find_all("div", {"class": "gs_r"})
	
	x = 1
	
	print("\n5 Most Popular Papers that Cite this Article:")
	for item in article:
		print("Paper %d: "%(x) + item.find_all("h3", {"class": "gs_rt"})[0].text.encode('ascii', 'ignore').decode('ascii'))
		if (x == 5):
			break
		x += 1	


	
		
if __name__ == "__main__":
	url = "https://scholar.google.co.uk/citations?view_op=view_citation&hl=en&user=G0yAJAwAAAAJ&citation_for_view=G0yAJAwAAAAJ:BqipwSGYUEgC"
	#url = "https://scholar.google.co.uk/citations?view_op=view_citation&hl=en&user=qc6CJjYAAAAJ&authuser=1&citation_for_view=qc6CJjYAAAAJ:u5HHmVD_uO8C"
	essayInformation(url)