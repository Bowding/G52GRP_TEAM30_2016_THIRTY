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
    #[0]ID [1]name [2]NumPaper [3]region/institution
    nodeSet = []
    #[0]sourceID [1]targetID
    linkSet = []

    targets = []


    #put sourceauthor in nodeSet first
    nodeSet.append([search,"","" ,"" ])


    #construct sources scholar to targetscholar first
    cur.execute("SELECT * FROM `connections` WHERE `sourceScholarID` = '" + search +"'")
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
                node[3] = row[4]


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
        nodeSetString += 'hlink: "https://scholar.google.co.uk/citations?user=' + node[0] + '"},'

    #contruct string for linkSet
    linkSetString = ""

    for link in linkSet:
        linkSetString += '{sourceId: "' + link[0] + '",'
        linkSetString += 'targetId: "' + link[1] + '"},'


    typesTitle = '"Region"'

    @route('/hello/123')
    def index():
        return template("force_d3js.html", nodeSetString = nodeSetString, linkSetString = linkSetString, typesTitle = typesTitle)
    run(host='localhost', port=8080)

    cur.close()
    conn.close()

else:
    print ("No Results Found On DB!!")
    
