#-*-coding:utf-8-*-
import codecs
import bottle
import bottle_pymysql
import pymysql
import html
import requests
import os
import sys
import subprocess
from bottle import template, static_file
from bs4 import BeautifulSoup
from time import sleep
import threading
import random
from graphviz import Digraph 
from graphviz import Graph 
import webbrowser 
from random import randint 

#to make the script compatible with python 2.7 
if sys.version_info[0] < 3:
	reload(sys)
	sys.setdefaultencoding('utf8')     

global conn, cur

#connect to db
def connect_to_db():
    try:
        print("Connecting to mySQL.....")
        conn = pymysql.connect(user="root", passwd="", host="127.0.0.1", port=3306, database="googlescholardb", charset='utf8')
        print("Connection established!")
        return conn
    except:
        print("Connection Failed!")


#generate valid url from the search keyword user entered
def get_target_url(search):
    #URL CHECK
    URLcase0 = search.startswith('https://scholar.google.co.uk/citations?user=')
    URLcase1 = search.startswith('https://scholar.google.com/citations?user=')
    URLcase2 = search.startswith('://scholar.google.com/citations?user=')
    URLcase3 = search.startswith('://scholar.google.com/citations?user=')
    URLcase4 = search.startswith(':/scholar.google.com/citations?user=')
    URLcase5 = search.startswith('scholar.google.com/citations?user=')
    URLcase6 = search.startswith('https://scholar.google.ae/citations?user=')
    URLcase7 = search.startswith('https://scholar.google.at/citations?user=')
    URLcase8 = search.startswith('https://scholar.google.be/citations?user=')
    URLcase9 = search.startswith('https://scholar.google.bg/citations?user=')
    URLcase10 = search.startswith('https://scholar.google.ca/citations?user=')
    URLcase11 = search.startswith('https://scholar.google.ch/citations?user=')
    URLcase12 = search.startswith('https://scholar.google.cl/citations?user=')
    URLcase13 = search.startswith('https://scholar.google.cn/citations?user=')
    URLcase14 = search.startswith('https://scholar.google.cz/citations?user=')
    URLcase15 = search.startswith('https://scholar.google.de/citations?user=')
    URLcase16 = search.startswith('https://scholar.google.dk/citations?user=')
    URLcase17 = search.startswith('https://scholar.google.es/citations?user=')
    URLcase18 = search.startswith('https://scholar.google.fi/citations?user=')
    URLcase19 = search.startswith('https://scholar.google.fr/citations?user=')
    URLcase20 = search.startswith('https://scholar.google.gr/citations?user=')
    URLcase21 = search.startswith('https://scholar.google.hk/citations?user=')
    URLcase22 = search.startswith('https://scholar.google.hn/citations?user=')
    URLcase23 = search.startswith('https://scholar.google.hr/citations?user=')
    URLcase24 = search.startswith('https://scholar.google.hu/citations?user=')
    URLcase25 = search.startswith('https://scholar.google.is/citations?user=')
    URLcase26 = search.startswith('https://scholar.google.it/citations?user=')
    URLcase27 = search.startswith('https://scholar.google.li/citations?user=')
    URLcase28 = search.startswith('https://scholar.google.lt/citations?user=')
    URLcase29 = search.startswith('https://scholar.google.lu/citations?user=')
    URLcase30 = search.startswith('https://scholar.google.lv/citations?user=')
    URLcase31 = search.startswith('https://scholar.google.nl/citations?user=')
    URLcase32 = search.startswith('https://scholar.google.no/citations?user=')
    URLcase33 = search.startswith('https://scholar.google.pk/citations?user=')
    URLcase34 = search.startswith('https://scholar.google.pl/citations?user=')
    URLcase35 = search.startswith('https://scholar.google.pt/citations?user=')
    URLcase36 = search.startswith('https://scholar.google.ro/citations?user=')
    URLcase37 = search.startswith('https://scholar.google.ru/citations?user=')
    URLcase38 = search.startswith('https://scholar.google.se/citations?user=')
    URLcase39 = search.startswith('https://scholar.google.si/citations?user=')
    URLcase40 = search.startswith('https://scholar.google.sk/citations?user=')
    URLcase41 = search.startswith('https://scholar.google.co.in/citations?user=')
    URLcase42 = search.startswith('https://scholar.google.co.id/citations?user=')
    URLcase43 = search.startswith('https://scholar.google.co.il/citations?user=')
    URLcase44 = search.startswith('https://scholar.google.co.za/citations?user=')
    URLcase45 = search.startswith('https://scholar.google.co.cr/citations?user=')
    URLcase46 = search.startswith('https://scholar.google.co.nz/citations?user=')
    URLcase47 = search.startswith('https://scholar.google.co.jp/citations?user=')
    URLcase48 = search.startswith('https://scholar.google.co.kr/citations?user=')

    errURLcase0 = search.startswith('www.')
    errURLcase1 = search.startswith('http')
    errURLcase2 = search.endswith(".co.uk")
    errURLcase3 = search.endswith(".com")
    errURLcase4 = search.endswith(".ae")
    errURLcase5 = search.endswith(".at")
    errURLcase6 = search.endswith(".be")
    errURLcase7 = search.endswith(".bg")
    errURLcase8 = search.endswith(".ca")
    errURLcase9 = search.endswith(".ch")
    errURLcase10 = search.endswith(".cl")
    errURLcase11 = search.endswith(".cn")
    errURLcase12 = search.endswith(".cz")
    errURLcase13 = search.endswith(".de")
    errURLcase14 = search.endswith(".dk")
    errURLcase15 = search.endswith(".es")
    errURLcase16 = search.endswith(".fi")
    errURLcase17 = search.endswith(".fr")
    errURLcase18 = search.endswith(".gr")
    errURLcase19 = search.endswith(".hk")
    errURLcase20 = search.endswith(".hn")
    errURLcase21 = search.endswith(".hr")
    errURLcase22 = search.endswith(".hu")
    errURLcase23 = search.endswith(".is")
    errURLcase24 = search.endswith(".it")
    errURLcase25 = search.endswith(".li")
    errURLcase26 = search.endswith(".lt")
    errURLcase27 = search.endswith(".lu")
    errURLcase28 = search.endswith(".lv")
    errURLcase29 = search.endswith(".nl")
    errURLcase30 = search.endswith(".no")
    errURLcase31 = search.endswith(".pk")
    errURLcase32 = search.endswith(".pl")
    errURLcase33 = search.endswith(".pt")
    errURLcase34 = search.endswith(".ro")
    errURLcase35 = search.endswith(".ru")
    errURLcase36 = search.endswith(".se")
    errURLcase37 = search.endswith(".si")
    errURLcase38 = search.endswith(".sk")
    errURLcase39 = search.endswith(".co.in")
    errURLcase40 = search.endswith(".co.id")
    errURLcase41 = search.endswith(".co.il")
    errURLcase42 = search.endswith(".co.za")
    errURLcase43 = search.endswith(".co.cr")
    errURLcase44 = search.endswith(".co.nz")
    errURLcase45 = search.endswith(".co.jp")
    errURLcase46 = search.endswith(".co.kr")

    if(URLcase0 or URLcase1 or URLcase2 or URLcase3 or URLcase4 or URLcase5 or URLcase6 or URLcase7 or URLcase8 or URLcase9 or URLcase10 or URLcase11 or URLcase12 
      or URLcase13 or URLcase14 or URLcase15 or URLcase16 or URLcase17 or URLcase18 or URLcase19 or URLcase20 or URLcase21 or URLcase22 or URLcase23 or URLcase24
      or URLcase25 or URLcase26 or URLcase27 or URLcase28 or URLcase29 or URLcase30 or URLcase31 or URLcase32 or URLcase33 or URLcase34 or URLcase35 or URLcase36 
      or URLcase37 or URLcase38 or URLcase39 or URLcase40 or URLcase41 or URLcase42 or URLcase43 or URLcase44 or URLcase45 or URLcase46 or URLcase47 or URLcase48): #If the user enters a link to a scholars page, it will return the link straightaway
        check_url = requests.get(search)
        check_url_soup = BeautifulSoup(check_url.content, "html.parser")
        check = check_url_soup.find_all("div", {"class": "gs_med"})
        #print(check)
        if ((not check) == False) and ("Please click here if you are not redirected within a few seconds." in check[0].text):
            err_msg = "Error: Invalid URL. Please enter valid Google Scholar profile URL. e.g. https://scholar.google.co.uk/citations?user=..."
            print(err_msg)
            return err_msg
        else: 
            print("URL Accepted!")
            return "https://scholar.google.co.uk/citations?user=" + search.split("user=")[1].split("AAAAJ")[0]
        
    elif(errURLcase0 or errURLcase1 or errURLcase2 or errURLcase3 or errURLcase4 or errURLcase5 or errURLcase6 or errURLcase7 or errURLcase8 or errURLcase9 or errURLcase10
         or errURLcase11 or errURLcase12 or errURLcase13 or errURLcase14 or errURLcase15 or errURLcase16 or errURLcase17 or errURLcase18 or errURLcase19 or errURLcase20
         or errURLcase21 or errURLcase22 or errURLcase23 or errURLcase24 or errURLcase25 or errURLcase26 or errURLcase27 or errURLcase28 or errURLcase29 or errURLcase30
         or errURLcase31 or errURLcase32 or errURLcase33 or errURLcase34 or errURLcase35 or errURLcase36 or errURLcase37 or errURLcase38 or errURLcase39 or errURLcase40
         or errURLcase41 or errURLcase42 or errURLcase43 or errURLcase44 or errURLcase45 or errURLcase46): #If the input is an invalid URL
         err_msg = "Error: Invalid URL. Please enter valid Google Scholar profile URL. e.g. https://scholar.google.co.uk/citations?user=..."
        print(err_msg)
        return err_msg

	#If the input is not a URL
    else:   
	#This part of the function pieces together a link for a scholars page on Google Scholar using the user search query

        #generate searching url
        keyword = search.replace(" ", "+")
        search_url = "https://scholar.google.co.uk/scholar?q=" + keyword

        #generate url of matching authors page
        search_r = requests.get(search_url)
        search_soup = BeautifulSoup(search_r.content, "html.parser")

        match_url_area = search_soup.find("h3", {"class": "gs_rt"})
    
        #check whether there is scholar matches the keyword
        if ((match_url_area == None)==True) or (match_url_area.text.startswith('User profiles for') == False):
            err_msg = "Error: Scholar '" + search + "' not found.\n\n"
            print("Scholar not found")
            return err_msg
        else:
            match_url = "https://scholar.google.co.uk" + match_url_area.find("a").get("href")

            #generate url of target author page
            match_r = requests.get(match_url)
            match_soup = BeautifulSoup(match_r.content, "html.parser")

            target_url_area = match_soup.find("h3", {"class": "gsc_1usr_name"})
            target_url = "https://scholar.google.co.uk" + target_url_area.find("a").get("href")

            return target_url

    
#def insert_to_db(pymydb, filename):
def insert_to_db(conn, cur, filename):

    #to make the script compatible with python 2.7
    if sys.version_info[0] < 3:
        f_read = codecs.open(filename, 'r', encoding = 'utf-8')
    else: 
        f_read = open(filename, 'r', encoding = 'utf-8')

    #read sql instruction from given file
    sql_instructions = f_read.readline()
    
    #execute instructions
    try:
        cur.execute(sql_instructions)
        conn.commit()
    except ValueError:
        print("Failed inserting...." + filename)

    f_read.close()


#execute author_network.py to scrape the coauthor network of the target author
def get_author_network(target_user_id):
    os.system("python author_network.py %s" % (target_user_id))


#execute scholar_data.py to scrape related info of the target author
def get_scholar_data(target_user_id):
    #target_url = get_target_url(search)
    #url = target_url.split("=")[1].split("&")[0]
    os.system("python scholar_data.py %s" % (target_user_id))


#create a bar chart of 8 most cited coauthor
def createBarChart(conn, cur, target_user_id):

    cur.execute("SELECT * FROM `connections` WHERE `sourceScholarID` = '" + target_user_id +"'")

    #Check if there is any result
    result = 0
    for row in cur:
        result += 1

    #If there has result
    if result == 0:
        bar_info = {'barSetString': ""}
    else:
        #[0]ID [1]name [2]NumPaper 
        barSet = []

        #construct sources scholar to targetscholar first
        cur.execute("SELECT * FROM `connections` WHERE `sourceScholarID` = '" + target_user_id +"'")
        for row in cur:
            
            #check if there is repeated ID
            repeat = 0

            for bar in barSet:
                if bar[0] == row[1]:
                    repeat = 1

            if repeat == 0:
                barSet.append([row[1],"" ,"" ])

        #store authors' info
        for bar in barSet:
            cur.execute("SELECT * FROM `profile` WHERE `authorID` = '" + bar[0] +"'")
            for row in cur:
                if row[5] == bar[0]:
                    #change name into short form
                    parse = row[0].split(" ")
                    name = ""
                    for x in range(0, len(parse)):
                        if x == 0:
                            name += parse[x][0]
                        elif x == (len(parse) - 1):
                            name += " " + parse[x] 

                    #put name and numPaper into the list
                    bar[1] = name
                    bar[2] = row[3]

        #sort and save only top 8 highest amount of papers published
        barSet = sorted(barSet, key=lambda l:l[2], reverse=True)
        barSet = barSet[:8]
        barSet = sorted(barSet, key=lambda l:l[2])


        #contruct string for nodeSet
        barSetString = ""

        for bar in barSet:
            barSetString += '{id: "' + bar[0]+'", '
            barSetString += 'name: "' + bar[1] + '", '
            barSetString += 'barLength: "' + str(bar[2]) + '", '
            barSetString += 'hlink: "https://scholar.google.co.uk/citations?user=' + bar[0] + '&"},'

        bar_info = {'barSetString': barSetString}
    return bar_info


#create a author network graph in view of different classificaton criterion
def create_coauthor_network(conn, cur, target_user_id, option):
    cur.execute("SELECT * FROM `connections` WHERE `sourceScholarID` = '" + target_user_id +"'")

    #Check if there is any result
    result = 0
    for row in cur:
        result += 1

    if result == 0:
        print("noooooooooo")
        return
    #If there has result
    else:

        #[0]ID [1]name [2]NumPaper [3]region/institution
        nodeSet = []
        #[0]sourceID [1]targetID
        linkSet = []

        targets = []

        #put sourceauthor in nodeSet first
        nodeSet.append([target_user_id,"","" ,"" ])

        #construct sources scholar to targetscholar first
        cur.execute("SELECT * FROM `connections` WHERE `sourceScholarID` = '" + target_user_id +"'")
        for row in cur:
            linkSet.append((row[0], row[1]))

            #check if there is repeated ID
            repeat = 0

            for node in nodeSet:
                if node[0] == row[1]:
                    repeat = 1

            if repeat == 0:
                nodeSet.append([row[1],"" ,"" ,"" ])
                targets.append(row[1])

        #store authors' info
        for node in nodeSet:
            cur.execute("SELECT * FROM `profile` WHERE `authorID` = '" + node[0] +"'")
            for row in cur:
                if row[5] == node[0]:
                    node[1] = row[0]
                    node[2] = row[1]
                    if option == 'region':
                        node[3] = row[4]

        if option == 'institution':
            #acess institution
            for node in nodeSet:
                cur.execute("SELECT * FROM `institutions` WHERE `scholarID` = '" + node[0] +"'")

                #parse the institution name and save 
                for row in cur:
                    parse = row[1].split(", ")
                    for parsed in parse:
                        if "University" in parsed:
                            node[3] = parsed.replace(":", "'")
                            break
                        else:
                            node[3] = "Unknown"


        #access relationship between target scholar
        for target in targets:
            query = "SELECT * FROM `connections` WHERE `sourceScholarID` = '" + target +"' AND ("
            idx = 0
            for target2 in targets:
                if idx == 0:
                    query += "targetScholarID = '" + target2 +"'"
                else:
                    query += " OR targetScholarID = '" + target2 +"'"
                idx += 1
            query += ")"
            cur.execute(query)

            for row in cur:
                linkSet.append((row[0], row[1]))

        #DEL repeated linkset
        idx1 = 0
        for link1 in linkSet:
            idx2 = 0
            for link2 in linkSet:
                if link1[0] == link2[0] and link1[1] == link2[1] and idx1 != idx2:
                    del linkSet[idx2]
                idx2 += 1
            idx1 += 1


        #contruct string for nodeSet
        nodeSetString = ""

        for node in nodeSet:
            nodeSetString += '{id: "' + node[0]+'", '
            nodeSetString += 'name: "' + node[1] + '", '
            nodeSetString += 'numPaper: "' + str(node[2]) + '", '
            nodeSetString += 'type: "' + node[3] + '", '
            nodeSetString += 'hlink: "https://scholar.google.co.uk/citations?user=' + node[0] + '&"},'

        #contruct string for linkSet
        linkSetString = ""

        for link in linkSet:
            linkSetString += '{sourceId: "' + link[0] + '",'
            linkSetString += 'targetId: "' + link[1] + '"},'

        typesTitle = '"Institution"'

        network_info = {'nodeSetString': nodeSetString, 'linkSetString': linkSetString}
        return network_info


#get data from db and and fromat them into a dictionary 
def template_info(conn, cur, target_user_id):

    #execute sql instruction
    try:
        cur.execute("SELECT * FROM `profile` WHERE `authorID` = '%s'" % target_user_id)
        conn.commit()
    except ValueError:
        print("Failed selecting....")

    #select data
    data = cur.fetchone()

    #check whether there is profile data for target author
    if(data == None):
        return
    else:
        authorName = data[0]
        numPaper = data[1]
        hIndex = data[2]
        citationNum = data[3]
        avatarURL = "https://scholar.google.co.uk" + data[6]

        #get coauthorNum
        try:
            cur.execute("SELECT * FROM `connections` WHERE `sourceScholarID` = '%s'" % target_user_id)
            conn.commit()
        except ValueError:
            print("Failed selecting....")

        targetsLinks = [] 
        for row in cur: 
            repeat = 0 
            for targetLink in targetsLinks: 
                if targetLink == row[1]: 
                    repeat = 1 

            if repeat == 0: 
                targetsLinks.append(row[1])

        coauthorNum = len(targetsLinks)
    
        info = {'authorName': authorName, 'numPaper': numPaper, 'hIndex': hIndex, 'citationNum': citationNum, 'coauthorNum': coauthorNum, 'avatarURL': avatarURL}

        return info


#display the index of the website
@bottle.route('/')
def login():
    return template("index.html")


#link all useful static files
@bottle.route('/<filename>.css')
def stylesheets(filename):
    return static_file('{}.css'.format(filename), root='./')

@bottle.route('/<filename>.png')
def stylesheets(filename):
    return static_file('{}.png'.format(filename), root='./')

@bottle.route('/<filename>.ico')
def stylesheets(filename):
    return static_file('{}.ico'.format(filename), root='./')


#try to connect to db
conn = connect_to_db() 
cur = conn.cursor()


#set the default encoding of the db to utf-8
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')


#main
@bottle.route('/test', method="POST")
@bottle.view('home.html')
def formhandler():

    #get the input from search bar, and try to gernerate valid url from it
    search = bottle.request.forms.get('search')
    target_url = get_target_url(search)

    #if unable to get url, directing to error page with appropriate error massage
    if(not target_url.startswith('https://scholar.google.co.uk/citations?user=')):
        err_msg = target_url
        return template("error.html", err_msg = err_msg)

    #if get a valid url, get the user ID of target scholar
    global target_user_id
    target_user_id = target_url.split("user=")[1].split("&")[0]

    #produce threads for get_author_network and get_scholar_data function
    threads = []  
    t2 = threading.Thread(target = get_author_network, args = (target_user_id, )) 
    t3 = threading.Thread(target = get_scholar_data, args = (target_user_id, )) 

    #try get the dictionary to be used to produce bar chart
    bar_info = createBarChart(conn, cur, target_user_id)

    #if successed, i.e. demanded data is already in db
    #cache hit
    if(bar_info != {'barSetString': ""}):  
        print("caching graph successful!")

        #combine two info dictionary into one
        info = template_info(conn, cur, target_user_id)
        info.update(bar_info)

    #if cache failed, do scraping
    else:
        print("caching graph failed!")

        #add scraping threads to thread array
        threads.append(t2)
        threads.append(t3)

    #actuate all threads in the array
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()

    #check whether previous cache failed or not
    if((t2 in threads) and (t3 in threads)): 

        #insert data into db
        insert_to_db(conn, cur, 'author_network.txt') 
        insert_to_db(conn, cur, 'scholar_data.txt') 

        #get the dictionary containing profile info
        info = template_info(conn, cur, target_user_id)

        #get the dictionary containing info to create bar chart
        bar_info = createBarChart(conn, cur, target_user_id)

        #combine two dictionary together
        info.update(bar_info)

    print('Scraping Job Done')

    return info


#create the coauthor network in terms of the classification criterion user have chosen
@bottle.post('/hello/graph')
@bottle.view('author_network.html')
def getGraphData(): 

    #get user's option for classification criterion
    option = bottle.request.forms.get("graphRelation") 

    #classify by institutions
    if option == "relation1": 
        graph_option = "institution"

        #generate graph 
        network_info = create_coauthor_network(conn, cur, target_user_id, "institution")
    
    #classify by regions
    if option == "relation2":  
        graph_option = "region"
        
        #generate graph 
        network_info = create_coauthor_network(conn, cur, target_user_id, "region")

    network_info.update({'option': graph_option})
 
    return network_info
 
 
bottle.run(host='localhost', port=8080)

#terminate connection with db
cur.close() 
conn.close()