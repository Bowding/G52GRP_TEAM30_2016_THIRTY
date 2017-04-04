#-*-coding:utf-8-*-
import bottle
import bottle_pymysql
import pymysql
import html
import requests
import os
import sys
import subprocess
from bottle import template, static_file, ResourceManager
from bs4 import BeautifulSoup
import threading
from time import sleep
import random

#following codes is only needed for python 2.x and only works for python 2.x
#reload(sys)
#sys.setdefaultencoding('utf8')     


#connect to db
def connect_to_db():

    try:
        print("Connecting to mySQL.....")
        conn = pymysql.connect(user="root", passwd="CHEERs0251", host="127.0.0.1", port=3306, database="googlescholardb")
        print("Connection established!")
        return conn
    except:
        print("Connection Failed!")


#    try:
#        print("Connecting to mySQL.....")
#        plugin = bottle_pymysql.Plugin(dbuser = 'root', dbpass = 'CHEERs0251', dbname = 'googlescholardb')
        #conn = pymysql.connect(host='localhost', db='googlescholardb', user='root', password='', cursorclass=pymysql.cursors.DictCursor)
#        bottle.install(plugin)
#        print("Connection established!")
#    except:
#        print("Connection Failed!")


def get_target_url(search):

#URL CHECK

    if(search.startswith('https://scholar.google.co.uk/citations?user=')==True) or (search.startswith('https://scholar.google.com/citations?user=')==True): #If the user enters a link to a scholars page, it will return the link straightaway
        check_url = requests.get(search)
        check_url_soup = BeautifulSoup(check_url.content, "html.parser")
        check = check_url_soup.find_all("div", {"class": "gs_med"})
        #print(check)
        if ((not check) == False) and ("Please click here if you are not redirected within a few seconds." in check[0].text):
            print("Error: Invalid URL. Please enter valid Google Scholar profile URL. e.g. https://scholar.google.co.uk/citations?user=...")
            sys.exit() 
        print("URL Accepted!")
        return search
        
    if((search.startswith('www.')==True) or (search.startswith('http')==True)):
        print("Error: Invalid URL. Please enter valid Google Scholar profile URL. e.g. https://scholar.google.co.uk/citations?user=...")
        sys.exit()
	
	#This part of the function pieces together a link for a scholars page on Google Scholar using the user search query

    #generate searching url
    keyword = search.replace(" ", "+")
    search_url = "https://scholar.google.co.uk/scholar?q=" + keyword

    #generate url of matching authors page
    search_r = requests.get(search_url)
    search_soup = BeautifulSoup(search_r.content, "html.parser")

    match_url_area = search_soup.find("h3", {"class": "gs_rt"})
    
    if ((match_url_area == None)==True) or (match_url_area.text.startswith('User profiles for') == False):
        print("Scholar '" + search + "' not found")
        sys.exit()
    
    match_url = "https://scholar.google.co.uk" + match_url_area.find("a").get("href")

    #generate url of target author page
    match_r = requests.get(match_url)
    match_soup = BeautifulSoup(match_r.content, "html.parser")

    target_url_area = match_soup.find("h3", {"class": "gsc_1usr_name"})
    target_url = "https://scholar.google.co.uk" + target_url_area.find("a").get("href")

    return target_url

#search = "www.google.com"
#get_target_url(search)
    
#def insert_to_db(pymydb, filename):
def insert_to_db(conn, cur, filename):
    
    f_read = open(filename, 'r', encoding = 'utf-8' )
    sql_instructions = f_read.readline()
    try:
        cur.execute(sql_instructions)
        conn.commit()
    except ValueError:
        print("Failed inserting...." + filename)

    f_read.close()

def get_profile_and_paper(target_user_id):

    global authorName

    f_pp = open('profile_and_paper.txt', 'w', encoding = 'utf-8')
    #f_pp.write("dhuiwehduieh")

    #target_url = get_target_url(search)

#    url = target_url.replace("oe=ASCII","oi=ao&cstart=0&pagesize=100")
    url = "https://scholar.google.co.uk/citations?user=" + target_user_id + "AAAAJ" + "&oi=ao&cstart=0&pagesize=100"

    #access to target author page - first page
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    #get profile
    name_data = soup.find_all("div", {"id": "gsc_prf_in"})[0]
    hIndex = soup.find_all("td", {"class": "gsc_rsb_std"})

    print("Author Name: " + name_data.text.encode('ascii', 'ignore').decode('ascii'))
    print("h-index (all time): " + hIndex[2].text)
    print("h-index (Since 2011): " + hIndex[3].text + "\n")

    x = 1
    cstart = 0
    while(1):
        article = soup.find_all("tr", {"class": "gsc_a_tr"})
        for item in article:
            paperName = item.find_all("a", {"class": "gsc_a_at"})[0].text.encode('ascii', 'ignore').decode('ascii')
#            print("Paper: " + str(x) + " " + paperName)
            year = item.find_all("td", {"class": "gsc_a_y"})[0].text.encode('ascii', 'ignore').decode('ascii')
#            print("Year: " + year)

            citationNumber = item.find_all("td", {"class": "gsc_a_c"})[0].text.encode('ascii', 'ignore').decode('ascii')
            seq_type = type(citationNumber)
            citationNumber = seq_type().join(filter(seq_type.isdigit, citationNumber))
            
            if citationNumber != "" and year != "":
#                print("Cited by: " + citationNumber)
#                print("INSERT into papers (paperName, author, yearPublished, numberOfCitations) VALUES ('%s','%s', %d, %d)\n" % (paperName, name_data.text, int(year), int(citationNumber)))
                try:
                    f_pp.write("INSERT into papers (paperName, author, yearPublished, numberOfCitations) VALUES ('%s','%s', %d, %d);" % (paperName.replace("'","\\\'"), name_data.text, int(year), int(citationNumber)))
                    #conn.commit()
                except ValueError:
                    print("Failed inserting....")   
            elif citationNumber == "" and year != "":
#                print("Cited by: 0")
#                print("INSERT into papers (paperName, author, yearPublished) VALUES ('%s','%s', %d)\n" % (paperName, name_data.text, int(year)))
                try:
                    f_pp.write("INSERT into papers (paperName, author, yearPublished) VALUES ('%s','%s', %d);" % (paperName.replace("'","\\\'"), name_data.text, int(year)))
                    #conn.commit()
                except ValueError:
                    print("Failed inserting....")
            elif year == "" and citationNumber != "":
#                print("No publish year")
#                print("INSERT into papers (paperName, author, numberOfCitations) VALUES ('%s','%s', %d)\n" % (paperName, name_data.text, int(citationNumber)))
                try:
                    f_pp.write("INSERT into papers (paperName, author, numberOfCitations) VALUES ('%s','%s', %d);" % (paperName.replace("'","\\\'"), name_data.text, int(citationNumber)))
                    #conn.commit()
                except ValueError:
                    print("Failed inserting....")
            else:
#                print("No publish year and citation number")
#                print("INSERT into papers (paperName, author) VALUES ('%s','%s')\n" % (paperName, name_data.text))
                try:
                    f_pp.write("INSERT into papers (paperName, author) VALUES ('%s','%s');" % (paperName.replace("'","\\\'"), name_data.text))
                    #conn.commit()
                except ValueError:
                    print("Failed inserting....")
                    
            x += 1

        #get this page paper number
        this_page_NumPaper_range = soup.find("span", {"id": "gsc_a_nn"}).text
		#s = "–".encode("utf-8")
		#print("======="+this_page_NumPaper_range.split("–")[0])

        this_page_NumPaper = int(this_page_NumPaper_range.split('–')[1])
        cstart +=100

        if(this_page_NumPaper < cstart):
            x -= 1
            break
        
        #get next page url
#        url = target_url.replace("oe=ASCII","oi=ao&cstart=%d&pagesize=100" % (cstart))
        url = "https://scholar.google.co.uk/citations?user=" + target_user_id + "AAAAJ" + "&oi=ao&cstart=%d&pagesize=100" % (cstart)
        #access to next page
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

    #print("\nINSERT INTO profile (aName, NumPaper, hIndex, authorURL) VALUES ('%s', %d, %d, '%s')\n" % (name_data.text, int(x), int(hIndex[2].text), target_url))
    try:
        f_pp.write("INSERT INTO profile (aName, NumPaper, hIndex, authorID) VALUES ('%s', %d, %d, '%s');" % (name_data.text, int(x), int(hIndex[2].text), target_user_id))
        #conn.commit()
    except:
        print("Failed inserting....")

    f_pp.close()

    authorName = name_data.text


def get_author_network(target_user_id):
    #target_url = get_target_url(search)
    #url = target_url.split("=")[1].split("&")[0]
    os.system("python author_network.py %s" % (target_user_id))

def get_scholar_data(target_user_id):
    #target_url = get_target_url(search)
    #url = target_url.split("=")[1].split("&")[0]
    os.system("python scholar_data.py %s" % (target_user_id))

def visualize(target_user_id):
    #os.system("python get_data.py %s" % (authorName))
    #string = get_data.get_string()
    #print("+++++++" + string) 
    #s2_out = subprocess.check_output([sys.executable, "get_data.py", str(10)])
    #f = open('myhtml.txt', 'r')
    #string = f.readline()  # python will convert \n to os.linesep
    #f.close()
     
    #print("++++++++" + str(s2_out))
    #return string
    #url = target_url.split("=")[1].split("&")[0]
    os.system("python gra_coauthor_relationship.py %s" % (target_user_id))
    f = open('img/coauthor_re.svg', 'r')
    string = f.readline()  # python will convert \n to os.linesep
    f.close()
    return string


#display website
@bottle.route('/')
def login():
    return template("index.html")

#link static files
@bottle.route('/<filename>.css')
def stylesheets(filename):
    return static_file('{}.css'.format(filename), root='./')

@bottle.route('/<filename>.png')
def stylesheets(filename):
    return static_file('{}.png'.format(filename), root='./')

@bottle.route('/<filename>.ico')
def stylesheets(filename):
    return static_file('{}.ico'.format(filename), root='./')



#handle user input
@bottle.route('/test', method="POST")
def formhandler():
    """Handle the form submission"""
    #get search keyword
    search = bottle.request.forms.get('search')
    target_url = get_target_url(search)
    target_user_id = target_url.split("user=")[1].split("AAAAJ")[0]

#    url = "https://scholar.google.co.uk/citations?user=" + target_user_id + "AAAAJ"
#    url = "https://scholar.google.co.uk/citations?user=" + target_user_id + "AAAAJ" + "&oi=ao&cstart=%d&pagesize=100" % (1)

#   return url

    conn = connect_to_db()
    cur = conn.cursor()
    
    #vis_result = visualize(target_url)

    vis_result = "No Results Found On DB!!"
    
    if(vis_result == "No Results Found On DB!!"):

        threads = []
        t1 = threading.Thread(target = get_profile_and_paper, args = (target_user_id, ))
        #authorName = get_profile_and_paper(search, pymydb).replace(" ", "+")
        threads.append(t1)
        t2 = threading.Thread(target = get_author_network, args = (target_user_id, ))
        threads.append(t2)
        t3 = threading.Thread(target = get_scholar_data, args = (target_user_id, ))
        threads.append(t3)

        for t in threads:
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join()

        insert_to_db(conn, cur, 'profile_and_paper.txt')
        insert_to_db(conn, cur, 'author_network.txt')
        insert_to_db(conn, cur, 'scholar_data.txt')

        cur.close()
        conn.close()

    #    insert_to_db(pymydb, 'authors_fields.txt')
    #    insert_to_db(pymydb, 'authors_institution.txt')
    #    insert_to_db(pymydb, 'author_papers_data.txt')
        
    #    string = visualize(authorName.replace(" ", "+"))
    #    if(string == "No Results Found On DB!!"):
    #        return string
    #    else:
    #        return template("nodes_basic.html", links = string)
        return "yaaayyyy!"
        visualize(target_url)

    # f_v = open('img/coauthor_re.svg', 'r')
    #    string = f_v.readline()
    #    print("=========="+string)
    #    f_v.close


        print('Scraping Job Done')


    bottle.TEMPLATES.clear()

    return template("img/coauthor_re.svg")

    #string = visualize(authorName)
    #if(string == "No Results Found On DB!!"):
    #    return string
    #else:
    #    return template("nodes_basic.html", links = string)

bottle.run(host='localhost', port=8080)