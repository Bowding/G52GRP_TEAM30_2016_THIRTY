#from bottle import route, run, template
import pymysql
import html
import sys

#construct-links function
global passString

string = ""
def conLinks(source, target,size , group):
    global string
    string += "{source: \"" + source + "\""
    string += ", target: \""+ target + "\""
    string += ", size: \"" + size + "\""
    string += ", group: \"" + group + "\"},"

if __name__ == "__main__":
    #connect to mysql
    try:
        print("Connecting to mySQL.....")
        conn = pymysql.connect(user="root", passwd="CHEERs0251", host="127.0.0.1", port=3306, database="googlescholardb")
        print("Connection established!")
    except:
        print("Connection Failed!")

    #Name going to be search
    #print(len(sys.argv))
    search = sys.argv[1].replace("+", " ")
    #print(search)

    #search = "Andrew J Parkes"

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

        for row in cur:
            conLinks(row[0], row[1], "0.4px" ,"orange")
            targets.append(row[1])


        #access other sources and targets
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
                conLinks(row[0], row[1], "0.09px", "yellow")

#        @route('/hello/123')
#        def index():
#            return template("nodes_basic.html", links = string)

#        run(host='localhost', port=8080)

        cur.close()
        conn.close()
        f = open('myhtml.txt', 'w')
        f.write(string)  # python will convert \n to os.linesep
        f.close()
       
    else:
        string = "No Results Found On DB!!"
        f = open('myhtml.txt', 'w')
        f.write(string)  # python will convert \n to os.linesep
        f.close()
        print ("No Results Found On DB!!")


