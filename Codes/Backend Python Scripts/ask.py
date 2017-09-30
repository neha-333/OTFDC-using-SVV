#!/usr/bin/python
import urllib2
import MySQLdb
from bs4 import BeautifulSoup

def askquery(query):
	req = urllib2.Request("http://www.ask.com/web?q="+query,headers={'User-Agent':"Google Chrome"})
	con=urllib2.urlopen(req)
	content = con.read()
	soup = BeautifulSoup(content)
	title=soup.find_all("h2",{"class":"web-result-title"})
	link=soup.find_all("p",{"class":"web-result-url"})
	para=soup.find_all("p",{"class":"web-result-description"})
	titles=[]
	links = []
	paras = []
	for t,l,p in zip(title,link,para):
		titles.append(t.find('a').getText())
		l1=l.getText()
		if l1[len(l1)-1] == "/":
			l1=l1[:len(l1)-1]
		links.append(l1)
		paras.append(p.getText())

	# Open database connection
	db = MySQLdb.connect(db='svvtest', user='root', passwd='', unix_socket="/opt/lampp/var/mysql/mysql.sock")

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# Drop table if it already exist using execute() method.
	cursor.execute("DROP TABLE IF EXISTS ask")

	# Create table as per requirement
	sql = """CREATE TABLE ask
	(
	ID int NOT NULL AUTO_INCREMENT,
	title text NOT NULL,
	link text,
	description text,
	PRIMARY KEY (ID)
	)"""

	cursor.execute(sql)

	for t,l,p in zip(titles,links,paras):	
		# Prepare SQL query to INSERT a record into the database.
		#sql = "INSERT INTO ask \
		#	(TITLE, LINK, DESC) \
		#	VALUES ('%s', '%s', '%s')" % (t,l,p)
		query = "INSERT INTO ask(title,link,description) " \
		    "VALUES(%s,%s,%s)"
		args = (t.encode('utf8'), l.encode('utf8'), p.encode('utf8'))
		try:
		   # Execute the SQL command
		   cursor.execute(query, args)
		   # Commit your changes in the database
		   print "inserted a row in ask!"
		   db.commit()
		except:
		   # Rollback in case there is any error
		   print "failed in ask"
		   db.rollback()

	# disconnect from server
	db.close()

