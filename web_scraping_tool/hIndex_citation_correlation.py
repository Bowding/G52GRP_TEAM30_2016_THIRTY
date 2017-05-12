# -*-coding:utf-8-*-
import codecs
import requests
import pymysql
import sys
from bs4 import BeautifulSoup
import threading
import re

# following codes is only needed for python 2.x and only works for python 2.x
reload(sys)
sys.setdefaultencoding('utf8')

hIndexValuesArray = []

global f_sd
global lock

#create lock
lock = threading.Lock()

# A breadth first search pattern has been implemented to find unique scholars who are related to the input scholar
def scrapePaperData(url):
    threads = []

    try:
        print("Connecting to mySQL.....")
        conn = pymysql.connect(host='localhost', db='googlescholardb', user='root', password='', cursorclass=pymysql.cursors.DictCursor)
        print("Connection established!")
    except:
        print("Connection Failed!")

    cur = conn.cursor()

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    #get scholarID
    user_id = url.split("user=")[1].split("&")[0]
    print(user_id)

    # for every paper listed on profile, get the paper title and author name
    for paper in soup.find_all("tr", {"class": "gsc_a_tr"}):
        paperName = paper.find_all("a", {"class": "gsc_a_at"})[0]

        paperTitle = paperName.text.encode('ascii', 'ignore').decode('ascii')

        author_data = paper.find_all("div", {"class": "gs_gray"})[0]
        authors = author_data.text.encode('ascii', 'ignore').decode('ascii')

        #parse coAuthor string
        coAuthors = parseCoAuthorsString(authors)

        #find out h-Index of each scholar
        hIndexValues = hIndex(coAuthors, cur)

        #calculate average h-Index of the paper scholars
        averagehIndex = sum(hIndexValues)/len(hIndexValues)

        #get paper citation number
        citationNumber = paper.find_all("td", {"class": "gsc_a_c"})[0].text.encode('ascii', 'ignore').decode('ascii')
        seq_type = type(citationNumber)
        citationNumber = seq_type().join(filter(seq_type.isdigit, citationNumber))

        paperName = paperTitle.replace("'", "\\\'")
        authorID = user_id.replace("'", "\\\'")

        #export data to database
        try:
            lock.acquire()
            f_sd.write("INSERT INTO hindexversuscitations (paperTitle, authorID, avghIndex, numberOfCitations) VALUES ('%s', '%s', %d, %d);" % (paperTitle, user_id, int(averagehIndex), int(citationNumber)))
            lock.release()
        except ValueError:
            print("Failed inserting....")

        conn.close()

def parseCoAuthorsString(scholarList):
    return scholarList.split(", ")

#get value from the database
def hIndex(scholars, cur, conn):
    for scholar in scholars:
        scholar = scholar.replace(" ","% ")

        try:
            cur.execute("SELECT `hIndex` FROM `profile` WHERE `aName` LIKE '" + scholar + "'")
            conn.commit()
        except ValueError:
            print("Failed selecting....")

        data = cur.fetchone()

        if (data == None):
            hIndexValuesArray.append(0)
        else:
            print("hIndex found")
            hIndextmp = data.get('hIndex')
            hIndexValuesArray.append(hIndextmp)

    return hIndexValuesArray

if __name__ == "__main__":

    # to make the script compatible with python 2.7
    if sys.version_info[0] < 3:
        f_sd = codecs.open('scatter_data.txt', 'w', encoding='utf-8')
    else:
        f_sd = open('scatter_data.txt', 'w', encoding='utf-8')

    # get argument as target_user_id
    url = sys.argv[1]

    scrapePaperData(url)
    f_sd.close()