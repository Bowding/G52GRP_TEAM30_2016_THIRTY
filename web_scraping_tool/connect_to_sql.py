import pymysql

try:
    print("Connecting to mySQL.....")
    conn = pymysql.connect(user="root", passwd="", host="127.0.0.1", port=3306, database="googlescholar")
    print("Connection established!")
except:
    print("Connection Failed!")

cur = conn.cursor()


try:
    cur.execute("INSERT INTO profile (aName, NumPaper, hIndex) VALUES ('test3', 13, 32), ('test2', 12343, 31)")
    conn.commit()
except:
    print("Failed inserting....")
    
#cur.execute("SELECT * FROM `profile`")
#cur.execute("ALTER TABLE profile AUTO_INCREMENT = 1")


for row in cur:
    print(row)

cur.close()
conn.close()
