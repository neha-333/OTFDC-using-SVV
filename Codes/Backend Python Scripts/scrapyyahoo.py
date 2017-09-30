#!/usr/bin/python
import urllib2
import MySQLdb
from bs4 import BeautifulSoup

def yahooquery(query):
	req = urllib2.Request("http://search.yahoo.com/search?p="+query,headers={'User-Agent':"Google Chrome"})
	con=urllib2.urlopen(req)
	content = con.read()
	soup = BeautifulSoup(content)
	title1=soup.find_all("div",{"class":"compTitle options-toggle"})
	title=[]
	for t in title1[:]:
		title.append(t.find("h3",{"class":"title"}))

	for t in title[:]:
		if (t.getText().find("Video Results") != -1):
			title.remove(t)
		if (t.getText().find("Image Results") != -1):
			title.remove(t)
		if (t.getText().find("Movie Series") != -1):
			title.remove(t)
		if (t.getText().find("News") != -1):
			title.remove(t)

	para=soup.find_all("p",{"class":"lh-16"})

	links = []
	titles=[]
	paras=[]
	for t,p in zip(title,para):
		a = t.find('a',href=True)
		titles.append(t.getText())
		paras.append(p.getText())
		if a:
			l1=a['href']
			if l1[len(l1)-1] == "/":
				l1=l1[:len(l1)-1]
			links.append(l1)

	# Open database connection
	db = MySQLdb.connect(db='svvtest', user='root', passwd='', unix_socket="/opt/lampp/var/mysql/mysql.sock")

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# Drop table if it already exist using execute() method.
	cursor.execute("DROP TABLE IF EXISTS yahoo")

	# Create table as per requirement
	sql = """CREATE TABLE yahoo
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
		#sql = "INSERT INTO yahoo \
		#	(TITLE, LINK, DESC) \
		#	VALUES ('%s', '%s', '%s')" % (t,l,p)
		query = "INSERT INTO yahoo(title,link,description) " \
		    "VALUES(%s,%s,%s)"
		args = (t.encode('utf8'), l.encode('utf8'), p.encode('utf8'))
		try:
		   # Execute the SQL command
		   cursor.execute(query, args)
		   # Commit your changes in the database
		   print "inserted a row in yahoo!"
		   db.commit()
		except:
		   # Rollback in case there is any error
		   print "failed"
		   db.rollback()

	# disconnect from server
	db.close()

