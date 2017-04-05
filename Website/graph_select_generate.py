from graphviz import Digraph
from graphviz import Graph
from bottle import route, run, template, post, request
import pymysql
import webbrowser
from random import randint

def FieldAuthorGraph(filename, authorName, targets, isPrintAuthor):
    global search

    institution = []
    insAu = []
    field = []
    fieldAu = []


    #include author when author is selected
    if isPrintAuthor == '1':
        
        #access author's field
        query = "SELECT * FROM `fields` WHERE `scholarID` = '" + search +"'"
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
        query = "SELECT * FROM `institutions` WHERE `scholarID` = '" + search +"'"
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
    aCluster.node(search)
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


htmlFileName = "dataviz"

#connect to mysql
try:
    print("Connecting to mySQL.....")
    conn = pymysql.connect(user="root", passwd="CHEERs0251", host="127.0.0.1", port=3306, database="googlescholardb")
    print("Connection established!")
except:
    print("Connection Failed!")


#Name going to be search
search = "G0yAJAw"

cur = conn.cursor()
cur.execute("SELECT * FROM `connections` WHERE `sourceScholarID` = '" + search +"'")

#Check if there is any result
result = 0
for row in cur:
    result += 1



if result > 0:
    #construct sources scholar first
    cur.execute("SELECT * FROM `connections` WHERE `sourceScholarID` = '" + search +"'")
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
    cur.execute("SELECT * FROM `profile` WHERE `authorID` = '" + search +"'")

    #author first
    for row in cur:
        authorName = row[0]
        break

    #coauthor next
    for targetLink in targetsLinks:
        cur.execute("SELECT * FROM `profile` WHERE `authorID` = '" + targetLink +"'")
        for row in cur:
            targets.append((row[0], targetLink))
            

    

    @route('/hello/creategraph')
    def index():
        authorHTML = '<input id="auBox" type="checkbox" name="authorBox" value="1" disabled="true">' + authorName
        coauthorHTML = ''
        target_counter = 0
        for target in targets:
            if target_counter == 0:
                coauthorHTML += '<input class="coauBox" type="checkbox" name="coauthorBox" value="'+str(target_counter)+'">' + target[0] + '</td></tr>'
            else:
                coauthorHTML += '<tr><td><input class="coauBox" type="checkbox" name="coauthorBox" value="'+str(target_counter)+'">' + target[0] + '</td></tr>'
            target_counter += 1
        return template("html/" + htmlFileName + ".html", authorHTML=authorHTML, coauthorHTML=coauthorHTML, target_counter=target_counter)

    

    @post('/hello/graph')
    def getGraphData():
        option = request.forms.get("graphRelation")
        authorOption = request.forms.get("authorBox")
        coauthorOptions = request.forms.getlist("coauthorBox")

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



    run(host='localhost', port=8080)

    cur.close()
    conn.close()    

else:
    print ("No Results Found On DB!!")
