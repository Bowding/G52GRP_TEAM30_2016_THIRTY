#-*-coding:utf-8-*-
#import codecs
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
import threading
from time import sleep
import random
from graphviz import Digraph 
from graphviz import Graph 
import webbrowser 
from random import randint 

#following codes is only needed for python 2.x and only works for python 2.x
#reload(sys)
#sys.setdefaultencoding('utf8')     

global conn, cur 
#connect to db
def connect_to_db():

    try:
        print("Connecting to mySQL.....")
        conn = pymysql.connect(user="root", passwd="CHEERs0251", host="127.0.0.1", port=3306, database="googlescholardb", charset='utf8')
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
    URLcase0 = search.startswith('https://scholar.google.co.uk/citations?user=')
    URLcase1 = search.startswith('https://scholar.google.com/citations?user=')
    URLcase2 = search.startswith('://scholar.google.com/citations?user=')
    URLcase3 = search.startswith('//scholar.google.com/citations?user=')
    URLcase4 = search.startswith('/scholar.google.com/citations?user=')
    URLcase5 = search.startswith('scholar.google.com/citations?user=')

    errURLcase0 = search.startswith('www.')
    errURLcase1 = search.startswith('http')

    if(URLcase0 or URLcase1 or URLcase2 or URLcase3 or URLcase4 or URLcase5): #If the user enters a link to a scholars page, it will return the link straightaway
        check_url = requests.get(search)
        check_url_soup = BeautifulSoup(check_url.content, "html.parser")
        check = check_url_soup.find_all("div", {"class": "gs_med"})
        #print(check)
        if ((not check) == False) and ("Please click here if you are not redirected within a few seconds." in check[0].text):
            err_msg = "Error: Invalid URL. Please enter valid Google Scholar profile URL. e.g. https://scholar.google.co.uk/citations?user=..."
            print(err_msg)
            return err_msg
            #sys.exit() 
        else: 
            print("URL Accepted!")
            return "https://scholar.google.co.uk/citations?user=" + search.split("user=")[1].split("AAAAJ")[0]
        
    elif(errURLcase0 or errURLcase1): #If the input is an invalid URL
        err_msg = "Error: Invalid URL. Please enter valid Google Scholar profile URL. e.g. https://scholar.google.co.uk/citations?user=..."
        print(err_msg)
        return err_msg
        #sys.exit()
	
    else:   #If the input is not a URL
	#This part of the function pieces together a link for a scholars page on Google Scholar using the user search query

        #generate searching url
        keyword = search.replace(" ", "+")
        search_url = "https://scholar.google.co.uk/scholar?q=" + keyword

        #generate url of matching authors page
        search_r = requests.get(search_url)
        search_soup = BeautifulSoup(search_r.content, "html.parser")

        match_url_area = search_soup.find("h3", {"class": "gs_rt"})
    
        if ((match_url_area == None)==True) or (match_url_area.text.startswith('User profiles for') == False):
            err_msg = "Error: Scholar '" + search + "' not found.\n\nTry to search using Google Scholar profile URL. e.g. https://scholar.google.co.uk/citations?user=..."
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

#search = "www.google.com"
#get_target_url(search)
    
#def insert_to_db(pymydb, filename):
def insert_to_db(conn, cur, filename):
    
    f_read = open(filename, 'r', encoding = 'utf-8')
    sql_instructions = f_read.readline()
    try:
        cur.execute(sql_instructions)
        conn.commit()
    except ValueError:
        print("Failed inserting...." + filename)

    f_read.close()

def get_profile_and_paper(target_user_id):

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


def get_author_network(target_user_id):
    #target_url = get_target_url(search)
    #url = target_url.split("=")[1].split("&")[0]
    os.system("python author_network.py %s" % (target_user_id))

def get_scholar_data(target_user_id):
    #target_url = get_target_url(search)
    #url = target_url.split("=")[1].split("&")[0]
    os.system("python scholar_data.py %s" % (target_user_id))

def FieldAuthorGraph(filename, authorName, targets, isPrintAuthor): 
 
    institution = [] 
    insAu = [] 
    field = [] 
    fieldAu = [] 
 
    #include author when author is selected 
    if isPrintAuthor == '1': 
         
        #access author's field 
        query = "SELECT * FROM `fields` WHERE `scholarID` = '" + viz_search +"'" 
        cur.execute(query) 
 
        for row in cur: 
 
            repeat = 0 
 
            #check when there are repeated field name 
            for fie in field: 
                if fie == row[1]: 
                    repeat = 1 
            if repeat == 0: 
                field.append(row[1]) 
 
            #check if repeated field name and author name 
            repeat = 0 
            for fA in fieldAu: 
                if authorName == fA[0] and row[1] == fA[1]: 
                    repeat = 1 
            if repeat == 0: 
                fieldAu.append((authorName, row[1])) 
 
        #access author's institution  
        query = "SELECT * FROM `institutions` WHERE `scholarID` = '" + viz_search +"'" 
        cur.execute(query) 
 
        for row in cur: 
            repeat = 0 
             
            #parse the institution name and save in "uni" 
            parse = row[1].split(", ") 
            for parsed in parse: 
                if "University" in parsed: 
                    uni = parsed 
                    break 
                else: 
                    uni = row[1] 
                     
             
            #check when there are repeated institution name 
            for ins in institution: 
                if ins == uni: 
                    repeat = 1 
                    break 
            if repeat == 0: 
                institution.append(uni) 
 
            #check if repeated institution name and author name 
            repeat = 0 
            for iA in insAu: 
                if authorName == iA[0] and uni == iA[1]: 
                    repeat = 1 
                    break 
            if repeat == 0: 
                insAu.append((authorName, uni)) 
     
    #access fields and scholars relationship 
    for element in targets: 
        query = "SELECT * FROM `fields` WHERE `scholarID` = '" + element[1] +"'" 
        cur.execute(query) 
 
        for row in cur: 
            repeat = 0 
 
            #check when there are repeated field name 
            for fie in field: 
                if fie == row[1]: 
                    repeat = 1 
            if repeat == 0: 
                field.append(row[1]) 
 
            #check if repeated field name and author name 
            repeat = 0 
            for fA in fieldAu: 
                if element[0] == fA[0] and row[1] == fA[1]: 
                    repeat = 1 
            if repeat == 0: 
                #find author's name 
                fieldAu.append((element[0], row[1])) 
 
    #access institutions and scholars relationship 
    for element in targets: 
        query = "SELECT * FROM `institutions` WHERE `scholarID` = '" + element[1] +"'" 
        cur.execute(query) 
 
        for row in cur: 
            repeat = 0 
             
            #parse the institution name and save in "uni" 
            parse = row[1].split(", ") 
            for parsed in parse: 
                if "University" in parsed: 
                    uni = parsed 
                    break 
                else: 
                    uni = row[1] 
                     
             
            #check when there are repeated institution name 
            for ins in institution: 
                if ins == uni: 
                    repeat = 1 
                    break 
            if repeat == 0: 
                institution.append(uni) 
 
            #check if repeated institution name and author name 
            repeat = 0 
            for iA in insAu: 
                if element[0] == iA[0] and uni == iA[1]: 
                    repeat = 1 
                    break 
            if repeat == 0: 
                insAu.append((element[0], uni)) 
 
    g = Graph('G') 
    colorAu= [] 
    cCluster = [] 
    clusterCounter = 0 
    colorNum = 1 
     
    #construct multiple clusters and construct its nodes 
    for ins in institution: 
        cCluster.append(Graph("cluster_" + str(clusterCounter))) 
        cCluster[clusterCounter].body.append('style=filled') 
        cCluster[clusterCounter].body.append("color=lightgrey") 
        cCluster[clusterCounter].body.append('label = "' + ins +'"') 
        cCluster[clusterCounter].node_attr.update(style="filled") 
 
        for iA in insAu: 
            #special case for the person it is searching for 
            if ins == iA[1] and iA[0] == authorName: 
                cCluster[clusterCounter].node(authorName, color = "cyan") 
                colorAu.append((authorName, "cyan")) 
                 
            elif ins == iA[1]: 
                cCluster[clusterCounter].node(iA[0], colorscheme="paired12",color = str(colorNum))  
                colorAu.append((iA[0], colorNum)) #give each author a color 
                #control colorNum 
                colorNum += 1 
                if colorNum >= 13: 
                    colorNum = 1 
        clusterCounter += 1 
 
    fieldCluster = Graph("cluster_" + str(clusterCounter+1)) 
    fieldCluster.body.append('style=filled') 
    fieldCluster.body.append("color=gray72") 
    fieldCluster.body.append('label = "Field of Study"') 
    fieldCluster.node_attr.update(style="filled") 
    for fie in field: 
        for fA in fieldAu: 
            if fA[0] == authorName and fA[1] == fie: 
                fieldCluster.node(fie, color="cyan") 
            else: 
                fieldCluster.node(fie) 
 
    for x in range(0, clusterCounter): 
        g.subgraph(cCluster[x]) 
    g.subgraph(fieldCluster) 
 
    for fA in fieldAu: 
        #find the color of that author 
        for cA in colorAu: 
            if fA[0] == cA[0]: 
                g.edge(fA[0],fA[1], colorscheme="paired12", color = str(cA[1]), penwidth="2") #create edge 
 
    g.body.append('ratio = compress') 
    g.body.append('size = "8,30"') 
    g.body.append(' rankdir="LR"') 
    g.body.append('splines=line') 
    #g.edge_attr.update(style='filled', color='green') 
    g.format = "svg" 
    g.render("img/"+filename) 
 
 
def CoAuGraph(filename, targets): 
    coAuthorR = [] 
    coAuthorRLinks = [] 
    institution = [] 
    insAu = [] 
     
    #access other source author and coauthors relationship 
    for element in targets: 
        query = "SELECT * FROM `connections` WHERE `sourceScholarID` = '" + element[1] +"' AND (" 
        idx = 0 
        for target in targets: 
            if idx == 0: 
                query += "targetScholarID = '" + target[1] +"'" 
            else: 
                query += " OR targetScholarID = '" + target[1] +"'" 
            idx += 1 
        query += ")" 
        cur.execute(query) 
 
        for row in cur: 
            #change id into name 
            for target in targets: 
                if target[1] == row[0]: 
                    rowZero = target[0] 
                if target[1] == row[1]: 
                    rowOne = target[0] 
                     
            #avoid repeated edges 
            repeat = 0 
            for coA in coAuthorR: 
                if (coA[0] == rowOne and coA[1] == rowZero) or (coA[0] == rowZero and coA[1] == rowOne): 
                    repeat = 1 
                     
            #if not repeated then insert the relationship 
            if repeat == 0: 
                         
                coAuthorR.append((rowZero, rowOne)) 
 
    #access institutions and scholars relationship 
    for target in targets: 
        query = "SELECT * FROM `institutions` WHERE `scholarID` = '" + target[1] +"'" 
        cur.execute(query) 
 
        for row in cur: 
            repeat = 0 
 
            #parse the institution name and save in "uni" 
            parse = row[1].split(", ") 
            for parsed in parse: 
                if "University" in parsed: 
                    uni = parsed 
                    break 
                else: 
                    uni = row[1] 
             
            #check when there are repeated institution name 
            for ins in institution: 
                if ins == uni: 
                    repeat = 1 
                    break 
            if repeat == 0: 
                institution.append(uni) 
 
            #check if repeated institution name and author name 
            repeat = 0 
            for iA in insAu: 
                if target[0] == iA[0] and uni == iA[1]: 
                    repeat = 1 
                    break 
            if repeat == 0: 
                insAu.append((target[0], uni)) 
 
    g = Graph('G') 
 
    cCluster = [] 
    clusterCounter = 0 
     
    #construct multiple clusters and construct its nodes 
    for ins in institution: 
        cCluster.append(Graph("cluster_" + str(clusterCounter))) 
        cCluster[clusterCounter].body.append('style=filled') 
        cCluster[clusterCounter].body.append("color=lightgrey") 
        cCluster[clusterCounter].body.append('label = "' + ins +'"') 
        cCluster[clusterCounter].node_attr.update(style="filled") 
 
        for iA in insAu: 
            if ins == iA[1]: 
                cCluster[clusterCounter].node(iA[0], fontsize = "13")  
        clusterCounter += 1 
 
    aCluster = Graph("cluster_"+ str(clusterCounter+1)) 
    aCluster.body.append('style=filled') 
    aCluster.body.append("color=orange") 
    aCluster.body.append('label = "Author"') 
    aCluster.node(viz_search) 
    aCluster.node_attr.update(style="filled") 
 
    for num in range(0,clusterCounter): 
        g.subgraph(cCluster[num]) 
 
    for cAR in coAuthorR: 
        g.edge(cAR[0], cAR[1], penwidth="1.7e") 
 
    g.body.append('ratio = compress') 
    g.body.append('size = "13,30"') 
    g.body.append(' rankdir="BT"') 
    g.body.append('splines=line') 
    #g.body.append('nodesep="0.3"') 
 
    g.format = "svg" 
    g.render("img/"+filename) 
 
 

def visualize(conn, cur, target_user_id): 
    
#    os.system("python gra_coauthor_relationship.py %s" % (target_user_id))
#    f = open('test.txt', 'w', encoding = 'utf-8')
#    string = f.readline()  # python will convert \n to os.linesep
#    f.close()
#    return string
    
    htmlFileName = "dataviz" 
    global targets, viz_search, authorName 
 
    #Name going to be search 
    viz_search = target_user_id 
 
    cur = conn.cursor() 
    cur.execute("SELECT * FROM `connections` WHERE `sourceScholarID` = '" + viz_search +"'") 
 
    #Check if there is any result 
    result = 0 
    for row in cur: 
        result += 1 
 
    if(result == 0): 
        return 
    else: 
        #construct sources scholar first 
        cur.execute("SELECT * FROM `connections` WHERE `sourceScholarID` = '" + viz_search +"'") 
        targetsLinks = [] 
         
        targets = [] 
 
 
        for row in cur: 
            repeat = 0 
            for targetLink in targetsLinks: 
                if targetLink == row[1]: 
                    repeat = 1 
 
            if repeat == 0: 
                targetsLinks.append(row[1]) 
 
        #search their name in database 
        #cur.execute("SELECT * FROM `profile` WHERE `authorID` = '" + viz_search +"'")
        try:
            cur.execute("SELECT * FROM `profile` WHERE `authorID` = '%s'" % viz_search)
            conn.commit()
        except ValueError:
            print("Failed selecting....") 
 
        #author first 
        #for row in cur: 
        #    authorName = row[0] 
        #    break 
        data = cur.fetchone()
        if(data == None):
            print("errrrrr!")
            sys.exit(1)
        else:
            authorName = data[0]
 
        #coauthor next 
        for targetLink in targetsLinks: 
            #cur.execute("SELECT * FROM `profile` WHERE `authorID` = '" + targetLink +"'") 
            try:
                cur.execute("SELECT * FROM `profile` WHERE `authorID` = '%s'" % targetLink)
                conn.commit()
            except ValueError:
                print("Failed selecting....")
            #for row in cur: 
            #    targets.append((row[0], targetLink)) 
            data = cur.fetchone()
            targets.append((data[0], targetLink))
 
        authorHTML = '<input id="auBox" type="checkbox" name="authorBox" value="1" disabled="true">' + authorName 
        coauthorHTML = '' 
        target_counter = 0 
        for target in targets: 
            if target_counter == 0: 
                coauthorHTML += '<input class="coauBox" type="checkbox" name="coauthorBox" value="'+str(target_counter)+'">' + target[0] + '</td></tr>' 
            else: 
                coauthorHTML += '<tr><td><input class="coauBox" type="checkbox" name="coauthorBox" value="'+str(target_counter)+'">' + target[0] + '</td></tr>' 
            target_counter += 1 
            #f.write(coauthorHTML)
        #t = template("html/" + htmlFileName + ".html", authorHTML=authorHTML, coauthorHTML=coauthorHTML, target_counter=target_counter) 
        vis_info = {'authorHTML': authorHTML, 'coauthorHTML':coauthorHTML, 'target_counter': target_counter}
        #f.close()
        return vis_info 
 
def template_info(conn, cur, target_user_id):
    try:
        cur.execute("SELECT * FROM `profile` WHERE `authorID` = '%s'" % target_user_id)
        conn.commit()
    except ValueError:
        print("Failed selecting....")

    data = cur.fetchone()

    if(data == None):
        return
    else:
        authorName = data[0]
        #print("#######" + authorName)
        numPaper = data[1]
        hIndex = data[2]
    
        info = {'authorName': authorName, 'numPaper': numPaper, 'hIndex': hIndex}
        #print(info)
        return info

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

conn = connect_to_db() 
cur = conn.cursor()

#conn.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')

#handle user input
@bottle.route('/test', method="POST")
@bottle.view('home.html')
def formhandler():
    """Handle the form submission"""

    #insert_to_db(conn, cur, 'scholar_data.txt')
    #return "hahaha"

    #get search keyword

    search = bottle.request.forms.get('search')
    target_url = get_target_url(search)

    #url checking
    if(not target_url.startswith('https://scholar.google.co.uk/citations?user=')):
        err_msg = target_url
        return err_msg

    #if url is valid
    target_user_id = target_url.split("user=")[1].split("AAAAJ")[0]

    #get_scholar_data(target_user_id)
    #return "hsdkjfhkshfkhak"

#    url = "https://scholar.google.co.uk/citations?user=" + target_user_id + "AAAAJ"
#    url = "https://scholar.google.co.uk/citations?user=" + target_user_id + "AAAAJ" + "&oi=ao&cstart=%d&pagesize=100" % (1)
#   return url

    threads = [] 
    #t1 = threading.Thread(target = get_profile_and_paper, args = (target_user_id, )) 
    t2 = threading.Thread(target = get_author_network, args = (target_user_id, )) 
    t3 = threading.Thread(target = get_scholar_data, args = (target_user_id, )) 


#    info = template_info(conn, cur, target_user_id)

#    vis_result = None
    vis_result = visualize(conn, cur, target_user_id)

#    if(info != None):   #cache hit
#        print("caching author profile successful!") 
#        vis_result = visualize(conn, cur, target_user_id, info) 
#    else: 
#        print("caching author profile failed!") 
#        threads.append(t1)

    if(vis_result != None): #cache hit 
        print("caching graph successful!")
        info = template_info(conn, cur, target_user_id)
        #print(profile_info)
        #print(vis_result)
        info.update(vis_result)
        #print(info)
        

    else:   #do scraping
        print("caching graph failed!") 
        threads.append(t2)
        threads.append(t3)

    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()


#    if(t1 in threads):
#        insert_to_db(conn, cur, 'profile_and_paper.txt')
#        info = template_info(conn, cur, target_user_id)

    if((t2 in threads) and (t3 in threads)): 
        insert_to_db(conn, cur, 'author_network.txt') 
        insert_to_db(conn, cur, 'scholar_data.txt') 
        vis_result = visualize(conn, cur, target_user_id) 
        info = template_info(conn, cur, target_user_id)
        info.update(vis_result)
        return info

    print('Scraping Job Done')
    #    insert_to_db(pymydb, 'authors_fields.txt')
    #    insert_to_db(pymydb, 'authors_institution.txt')
    #    insert_to_db(pymydb, 'author_papers_data.txt')
        
    #    string = visualize(authorName.replace(" ", "+"))
    #    if(string == "No Results Found On DB!!"):
    #        return string
    #    else:
    #        return template("nodes_basic.html", links = string)
        #return "yaaayyyy!"
        #visualize(target_url)

    # f_v = open('img/coauthor_re.svg', 'r')
    #    string = f_v.readline()
    #    print("=========="+string)
    #    f_v.close


        


#    bottle.TEMPLATES.clear()

#    return template("img/coauthor_re.svg")

    return info
    #string = visualize(authorName)
    #if(string == "No Results Found On DB!!"):
    #    return string
    #else:
    #    return template("nodes_basic.html", links = string)

@bottle.post('/hello/graph') 
def getGraphData(): 
    option = bottle.request.forms.get("graphRelation") 
    authorOption = bottle.request.forms.get("authorBox") 
    coauthorOptions = bottle.request.forms.getlist("coauthorBox") 
 
    #check what target schlors are selected and put them into selectedSchlors 
    selectedSchlors = [] 
    for coauthorOption in coauthorOptions: 
        selectedSchlors.append((targets[int(coauthorOption)][0], targets[int(coauthorOption)][1])) 
 
    #set authorOption to zero when it is empty 
    if authorOption == None: 
        authorOption = 0 
 
         
    if option == "relation1": 
        filename = "coauthor_re" + str(randint(0,10000)) 
             
        #generate graph 
        CoAuGraph(filename, selectedSchlors) 
             
    if option == "relation2": 
        filename = "field_coauthor" + str(randint(0,10000)) 
 
        #generate graph 
        FieldAuthorGraph(filename, authorName, targets, authorOption) 
 
    return template("img/" + filename + ".svg") 
 
 
bottle.run(host='localhost', port=8080)
 
cur.close() 
conn.close()