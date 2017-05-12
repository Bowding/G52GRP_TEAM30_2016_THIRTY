from graphviz import Digraph
from graphviz import Graph
from bottle import route, run, template
import pymysql


#connect to mysql
try:
    print("Connecting to mySQL.....")
    conn = pymysql.connect(user="root", passwd="CHEERs0251", host="127.0.0.1", port=3306, database="googlescholardb")
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
    field = []
    fieldAu = []
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

    #access fields and scholars relationship
    for element in targets:
        query = "SELECT * FROM `fields` WHERE `scholarName` = '" + element +"'"
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
                if row[0] == fA[0] and row[1] == fA[1]:
                    repeat = 1
            if repeat == 0:
                fieldAu.append((row[0], row[1]))
    

    #access author's field
    query = "SELECT * FROM `fields` WHERE `scholarName` = '" + search +"'"
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
            if row[0] == fA[0] and row[1] == fA[1]:
                repeat = 1
        if repeat == 0:
            fieldAu.append((row[0], row[1]))

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

    #access author's institution 
    query = "SELECT * FROM `institutions` WHERE `scholarName` = '" + search +"'"
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
            

    
    filename = "field_coauthor"

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
            if ins == iA[1] and iA[0] == search:
                cCluster[clusterCounter].node(search, color = "cyan")
                colorAu.append((search, "cyan"))
                
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
            if fA[0] == search and fA[1] == fie:
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
                print(cA)
                g.edge(fA[0],fA[1], colorscheme="paired12", color = str(cA[1]), penwidth="2") #create edge

    g.body.append('ratio = compress')
    g.body.append('size = "9,30"')
    g.body.append(' rankdir="LR"')
    g.body.append('splines=ortho')
    #g.edge_attr.update(style='filled', color='green')
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
    
