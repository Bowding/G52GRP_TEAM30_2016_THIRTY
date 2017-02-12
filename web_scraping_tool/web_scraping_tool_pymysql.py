import pymysql
import requests
from bs4 import BeautifulSoup

url = "https://scholar.google.co.uk/citations?user=G0yAJAwAAAAJ&hl=en&oi=ao&cstart=0&pagesize=200"

r = requests.get(url)

soup = BeautifulSoup(r.content, "html.parser")

name_data = soup.find_all("div", {"id": "gsc_prf_in"})[0]
hIndex = soup.find_all("td", {"class": "gsc_rsb_std"})
article = soup.find_all("tr", {"class": "gsc_a_tr"})

print("Author Name: " + name_data.text)
print("h-index (all time): " + hIndex[2].text)
print("h-index (Since 2011): " + hIndex[3].text + "\n")

try:
	print("Connecting to mySQL.....")
	conn = pymysql.connect(host='localhost', db='googlescholardb', user='root', password='', cursorclass=pymysql.cursors.DictCursor)
	print("Connection established!")
except:
	print("Connection Failed!")

cur = conn.cursor()

x = 1
for item in article:
	paperName = item.find_all("a", {"class": "gsc_a_at"})[0].text.encode('ascii', 'ignore').decode('ascii')
	print("Paper: " + str(x) + " " + paperName)
	year = item.find_all("td", {"class": "gsc_a_y"})[0].text.encode('ascii', 'ignore').decode('ascii')
	print("Year: " + year)
	
	citationNumber = item.find_all("td", {"class": "gsc_a_c"})[0].text.encode('ascii', 'ignore').decode('ascii')
	seq_type = type(citationNumber)
	citationNumber = seq_type().join(filter(seq_type.isdigit, citationNumber))
	
	if citationNumber != "":
		print("Cited by: " + citationNumber)
		print("INSERT into papers (paperName, author, yearPublished, numberOfCitations) VALUES ('%s','%s', %d, %d)\n" % (paperName, name_data.text, int(year), int(citationNumber)))
		try:
			cur.execute("INSERT into papers (paperName, author, yearPublished, numberOfCitations) VALUES ('%s','%s', %d, %d)" % (paperName, name_data.text, int(year), int(citationNumber)))
			conn.commit()
		except ValueError:
			print("Failed inserting....")	
	else:
		print("Cited by: 0")
		print("INSERT into papers (paperName, author, yearPublished) VALUES ('%s','%s', %d)\n" % (paperName, name_data.text, int(year)))
		try:
			cur.execute("INSERT into papers (paperName, author, yearPublished) VALUES ('%s','%s', %d)" % (paperName, name_data.text, int(year)))
			conn.commit()
		except ValueError:
			print("Failed inserting....")	
			
	x += 1

print("\nINSERT INTO profile (aName, NumPaper, hIndex) VALUES ('%s', %d, %d)\n" % (name_data.text, int(x), int(hIndex[2].text)))
try:
	cur.execute("INSERT INTO profile (aName, NumPaper, hIndex) VALUES ('%s', %d, %d)" % (name_data.text, int(x), int(hIndex[2].text)))
	conn.commit()
except:
	print("Failed inserting....")
	
cur.execute("SELECT * FROM `profile`")
for row in cur:
	print(row)

print("\n")
	
cur.execute("SELECT * FROM `papers`")
for row in cur:
	print(row)

cur.close()
conn.close()