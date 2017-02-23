import pymysql

try:
	print("Connecting to mySQL.....")
	conn = pymysql.connect(host='localhost', db='googlescholardb', user='root', password='', cursorclass=pymysql.cursors.DictCursor)
	print("Connection established!")
except:
	print("Connection Failed!")

cur = conn.cursor()

object = open("graph_data_googleScholar.json", "w")
object.write('{\n  "nodes": [ \n')

cur.execute("SELECT COUNT(*) FROM `nodes`")
for row in cur:
	for key, value in row.items():
		rows = value
		print value

count = 0

cur.execute("SELECT * FROM `nodes`")
for row in cur:
	for key, value in row.items():
		if count < rows-1:
			object.write('    {"id": ' + '"' + value + '",' + ' "group": 1},\n')
			count += 1
		else:
			object.write('    {"id": ' + '"' + value + '",' + ' "group": 1}\n')
			count = 0

object.write('  ],\n  "links": [ \n')
	
cur.execute("SELECT COUNT(*) FROM `connections`")
for row in cur:
	for key, value in row.items():
		rows = value
		if rows > 256:
			rows = 256 
		print value
		
cur.execute("SELECT * FROM `connections`")
for row in cur:
	i = 0
	for key, value in row.items():
		if i == 0:
			target = value
			i += 1
		elif i == 1:
			source = value
			
	if count < rows-1:
		object.write('    {"source": "' + source + '", "target": "' + target + '", "value": 1},\n')
		count += 1
	else:
		object.write('    {"source": "' + source + '", "target": "' + target + '", "value": 1}\n')
		break
		
object.write('  ]\n}')

object.close()
cur.close()
conn.close()