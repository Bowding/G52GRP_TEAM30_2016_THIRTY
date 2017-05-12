from graphviz import Digraph
from graphviz import Graph
from bottle import route, run, template
import pymysql


#connect to mysql
try:
    print("Connecting to mySQL.....")
    conn = pymysql.connect(user="root", passwd="", host="127.0.0.1", port=3306, database="googlescholardb")
    print("Connection established!")
except:
    print("Connection Failed!")


#Name going to be search
search = "Andrew J Parkes"

cur = conn.cursor()
cur.execute("SELECT * FROM `connections` WHERE `sourceScholar` = '" + search +"'")

#Check if there is any result
result = 0
for row in cur:
    result += 1



if result > 0:
    #construct sources scholar first
    cur.execute("SELECT * FROM `connections` WHERE `sourceScholar` = '" + search +"'")
    targets = []

    institution = []
    insAu = []
    coAuthorR = []
    AuthorR = []
    for row in cur:
        AuthorR.append((row[0], row[1]))

        repeat = 0
        for target in targets:
            if target == row[1]:
                repeat = 1

        if repeat == 0:
            targets.append(row[1])

    print(targets)
    #access other source author and coauthors relationship
    for element in targets:
        query = "SELECT * FROM `connections` WHERE `sourceScholar` = '" + element +"' AND ("
        idx = 0
        for target in targets:
            if idx == 0:
                query += "targetScholar = '" + target +"'"
            else:
                query += " OR targetScholar = '" + target +"'"
            idx += 1
        query += ")"
        cur.execute(query)

        for row in cur:
            #avoid repeated edges
            repeat = 0
            for coA in coAuthorR:
                if coA[0] == row[1] and coA[1] == row[0]:
                    repeat = 1

            #if not repeated then insert the relationship
            if repeat == 0:
                coAuthorR.append((row[0], row[1]))


    #access institutions and scholars relationship
    for element in targets:
        query = "SELECT * FROM `institutions` WHERE `scholarName` = '" + element +"'"
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
                if row[0] == iA[0] and uni == iA[1]:
                    repeat = 1
                    break
            if repeat == 0:
                insAu.append((row[0], uni))


    filename = "coauthor_re"

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
    aCluster.node(search)
    aCluster.node_attr.update(style="filled")


    for num in range(0,clusterCounter):
        g.subgraph(cCluster[num])
    #g.subgraph(aCluster)

    for cAR in coAuthorR:
        g.edge(cAR[0], cAR[1], penwidth="2")

    g.body.append('ratio = compress')
    g.body.append('size = "13,30"')
    g.body.append(' rankdir="BT"')
    g.body.append('splines=ortho')
    #g.body.append('nodesep="0.3"')


    g.format = "svg"
    g.render("img/"+filename)

    @route('/hello/123')
    def index():
        return template("img/" + filename + ".svg")
    run(host='localhost', port=8080)

    cur.close()
    conn.close()

else:
    print ("No Results Found On DB!!")
    
