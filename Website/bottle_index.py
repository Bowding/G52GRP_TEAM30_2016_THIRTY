import bottle
import bottle_pymysql
import requests
from bottle import template, static_file
from bs4 import BeautifulSoup


@bottle.route('/')
def login():
    return template("index.html")

@bottle.route('/<filename>')
def stylesheets(filename):
    return static_file(filename, root = '/')

try:
    print("Connecting to mySQL.....")
    plugin = bottle_pymysql.Plugin(dbuser = 'root', dbpass = 'CHEERs0251', dbname = 'googlescholardb')
    #conn = pymysql.connect(host='localhost', db='googlescholardb', user='root', password='', cursorclass=pymysql.cursors.DictCursor)
    bottle.install(plugin)
    print("Connection established!")
except:
    print("Connection Failed!")

    #cur = conn.cursor()




@bottle.route('/test', method="POST")
def formhandler(pymydb):
    """Handle the form submission"""
    #get search keyword
    search = bottle.request.forms.get('search')
    
    #generate searching url
    keyword = search.replace(" ", "+")
    search_url = "https://scholar.google.co.uk/scholar?q=" + keyword

    #generate url of matching authors page
    search_r = requests.get(search_url)
    search_soup = BeautifulSoup(search_r.content, "html.parser")

    match_url_area = search_soup.find("h3", {"class": "gs_rt"})
    match_url = "https://scholar.google.co.uk" + match_url_area.find("a").get("href")

    #generate url of target author page
    match_r = requests.get(match_url)
    match_soup = BeautifulSoup(match_r.content, "html.parser")

    target_url_area = match_soup.find("h3", {"class": "gsc_1usr_name"})
    target_url = "https://scholar.google.co.uk" + target_url_area.find("a").get("href")
    #access to target author page
    r = requests.get(target_url)
    soup = BeautifulSoup(r.content, "html.parser")

    name_data = soup.find_all("div", {"id": "gsc_prf_in"})[0]
    hIndex = soup.find_all("td", {"class": "gsc_rsb_std"})
    article = soup.find_all("tr", {"class": "gsc_a_tr"})

    print("Author Name: " + name_data.text)
    print("h-index (all time): " + hIndex[2].text)
    print("h-index (Since 2011): " + hIndex[3].text + "\n")

    x = 1
    for item in article:
        paperName = item.find_all("a", {"class": "gsc_a_at"})[0].text.encode('ascii', 'ignore').decode('ascii')
        print("Paper: " + str(x) + " " + paperName)
        year = item.find_all("td", {"class": "gsc_a_y"})[0].text.encode('ascii', 'ignore').decode('ascii')
        print("Year: " + year)

        citationNumber = item.find_all("td", {"class": "gsc_a_c"})[0].text.encode('ascii', 'ignore').decode('ascii')
        seq_type = type(citationNumber)
        citationNumber = seq_type().join(filter(seq_type.isdigit, citationNumber))
        
        if citationNumber != "" and year != "":
            print("Cited by: " + citationNumber)
            print("INSERT into papers (paperName, author, yearPublished, numberOfCitations) VALUES ('%s','%s', %d, %d)\n" % (paperName, name_data.text, int(year), int(citationNumber)))
            try:
                pymydb.execute("INSERT into papers (paperName, author, yearPublished, numberOfCitations) VALUES ('%s','%s', %d, %d)" % (paperName, name_data.text, int(year), int(citationNumber)))
                #conn.commit()
            except ValueError:
                print("Failed inserting....")   
        elif citationNumber == "":
            print("Cited by: 0")
            print("INSERT into papers (paperName, author, yearPublished) VALUES ('%s','%s', %d)\n" % (paperName, name_data.text, int(year)))
            try:
                pymydb.execute("INSERT into papers (paperName, author, yearPublished) VALUES ('%s','%s', %d)" % (paperName, name_data.text, int(year)))
                #conn.commit()
            except ValueError:
                print("Failed inserting....")
        elif year == "":
            print("No publish year")
            print("INSERT into papers (paperName, author, numberOfCitations) VALUES ('%s','%s', %d)\n" % (paperName, name_data.text, int(citationNumber)))
            try:
                pymydb.execute("INSERT into papers (paperName, author, numberOfCitations) VALUES ('%s','%s', %d)" % (paperName, name_data.text, int(citationNumber)))
                #conn.commit()
            except ValueError:
                print("Failed inserting....")
        else:
            print("No publish year and citation number")
            print("INSERT into papers (paperName, author) VALUES ('%s','%s')\n" % (paperName, name_data.text))
            try:
                pymydb.execute("INSERT into papers (paperName, author) VALUES ('%s','%s')" % (paperName, name_data.text))
                #conn.commit()
            except ValueError:
                print("Failed inserting....")
                
        x += 1

    print("\nINSERT INTO profile (aName, NumPaper, hIndex) VALUES ('%s', %d, %d)\n" % (name_data.text, int(x), int(hIndex[2].text)))
    try:
        pymydb.execute("INSERT INTO profile (aName, NumPaper, hIndex) VALUES ('%s', %d, %d)" % (name_data.text, int(x), int(hIndex[2].text)))
        #conn.commit()
    except:
        print("Failed inserting....")
        
    #pymydb.execute("SELECT * FROM `profile`")
    #cur = pymydb.fetchall()
    #for row in cur:
    #    print(row)

    #print("\n")
        
    #pymydb.execute("SELECT * FROM `papers`")
    #cur = pymydb.fetchall()
    #for row in cur:
    #    print(row)

    #cur.close()
    #conn.close()
    return search


bottle.run(host='localhost', port=8080)