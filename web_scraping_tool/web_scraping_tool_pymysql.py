import pymysql
import requests
from bs4 import BeautifulSoup

url = "https://scholar.google.co.uk/citations?user=G0yAJAwAAAAJ&hl=en&oi=ao&cstart=0&pagesize=200"

r = requests.get(url)

soup = BeautifulSoup(r.content)

name_data = soup.find_all("div", {"id": "gsc_prf_in"})[0]
hIndex = soup.find_all("td", {"class": "gsc_rsb_std"})
article = soup.find_all("tr", {"class": "gsc_a_tr"})

print("Author Name: " + name_data.text)
print("h-index (all time): " + hIndex[2].text)
print("h-index (Since 2011): " + hIndex[3].text + "\n")

x = 1

for item in article:
    print("Paper %d: "%(x) + item.find_all("a", {"class": "gsc_a_at"})[0].text)
    print("Year: " + item.find_all("td", {"class": "gsc_a_y"})[0].text)
    if item.find_all("td", {"class": "gsc_a_c"})[0].text != " ":
        print("Cited by: " + item.find_all("td", {"class": "gsc_a_c"})[0].text + "\n")
    else:
        print("Cited by: 0\n")
    x += 1



name = name_data.text
h = hIndex[2].text

try:
    print("Connecting to mySQL.....")
    conn = pymysql.connect(user="root", passwd="", host="127.0.0.1", port=3306, database="googlescholar")
    print("Connection established!")
except:
    print("Connection Failed!")

cur = conn.cursor()

print("INSERT INTO profile (aName, NumPaper, hIndex) VALUES ('%s', %d, %d)" %(name, int(x), int(h)))

try:
    cur.execute("INSERT INTO profile (aName, NumPaper, hIndex) VALUES ('%s', %d, %d)" %(name, int(x), int(h)))
    conn.commit()
except:
    print("Failed inserting....")
    
cur.execute("SELECT * FROM `profile`")


for row in cur:
    print(row)

cur.close()
conn.close()
