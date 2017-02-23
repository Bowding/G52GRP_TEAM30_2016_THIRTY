from bottle import route, run, template

@route('/pythonWebEnd.py?first_name=<name>')
def index(name):
	print name
	return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=8080)

#input box to type in url
#url is fed into web scraping tool
#information retrieved via the database