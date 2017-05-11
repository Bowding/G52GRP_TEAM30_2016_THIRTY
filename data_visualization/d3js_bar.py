from bottle import route, run, template
import pymysql
import html


#AuthorID going to be search
search = "8maqKdgAAAAJ"

#connect to mysql
try:
    print("Connecting to mySQL.....")
    conn = pymysql.connect(user="root", passwd="", host="127.0.0.1", port=3306, database="googlescholardb", charset='utf8')
    print("Connection established!")
except:
    print("Connection Failed!")

cur = conn.cursor()
cur.execute("SELECT * FROM `connections` WHERE `sourceScholarID` = '" + search +"'")

#Check if there is any result
result = 0
for row in cur:
    result += 1

#If there has result
if result > 0:
    #[0]ID [1]name [2]NumPaper 
    barSet = []


    #construct sources scholar to targetscholar first
    cur.execute("SELECT * FROM `connections` WHERE `sourceScholarID` = '" + search +"'")
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
                bar[2] = row[2]

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
        barSetString += 'hlink: "https://scholar.google.co.uk/citations?user=' + bar[0] + 'AAAAJ&"},'


    print(barSetString)

    @route('/hello/123')
    def index():
        return template("bar_python.html", barSetString = barSetString)
    run(host='localhost', port=8080)

    cur.close()
    conn.close()

else:
    print ("No Results Found On DB!!")
    
