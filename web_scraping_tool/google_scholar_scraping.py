import requests
from bs4 import BeautifulSoup
	
def basicInformation(url):
	r = requests.get(url)

	soup = BeautifulSoup(r.content, "html.parser")

	name_data = soup.find_all("div", {"id": "gsc_prf_in"})[0]
	hIndex = soup.find_all("td", {"class": "gsc_rsb_std"})
	article = soup.find_all("tr", {"class": "gsc_a_tr"})

	print("Author Name: " + name_data.text)
	print("h-index (all time): " + hIndex[2].text)
	print("h-index (Since 2011): " + hIndex[3].text + "\n")

	x = 1

	for item in article:
		print("Paper %d: "%(x) + item.find_all("a", {"class": "gsc_a_at"})[0].text.encode('ascii', 'ignore').decode('ascii'))
		print("Year: " + item.find_all("td", {"class": "gsc_a_y"})[0].text.encode('ascii', 'ignore').decode('ascii'))
		if item.find_all("td", {"class": "gsc_a_c"})[0].text != " ":
			print("Cited by: " + item.find_all("td", {"class": "gsc_a_c"})[0].text.encode('ascii', 'ignore').decode('ascii'))
		else:
			print("Cited by: 0\n")
		print("Co-Authors: " + item.find_all("div", {"class" : "gs_gray"})[0].text.encode('ascii', 'ignore').decode('ascii') + "\n")
		x += 1	
		
	for link in soup.find_all("a", {"class": "gsc_rsb_aa"}):
		link = "https://scholar.google.co.uk" + link.get('href')
		print(link)
		#basicInformation(link) 
		
if __name__ == "__main__":
	url = "https://scholar.google.co.uk/citations?user=33ftCdEAAAAJ&hl=en"
	basicInformation(url)