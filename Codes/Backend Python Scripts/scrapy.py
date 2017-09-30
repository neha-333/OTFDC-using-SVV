#!/usr/bin/python
import urllib2
import MySQLdb
from bs4 import BeautifulSoup

def bingquery(query):
	req = urllib2.Request("http://www.bing.com/search?q="+query,headers={'User-Agent':"Google Chrome"})
	con=urllib2.urlopen(req)
	content = con.read()
	soup = BeautifulSoup(content)
	title=soup.find_all("h2",{"class":""})
	for t in title[:]:
		if (t.getText().find("Videos of") != -1):
			title.remove(t)
		if (t.getText().find("Images of") != -1):
			title.remove(t)
		if (t.getText().find("Local results") != -1):
			title.remove(t)
		if (t.getText().find("News about") != -1):
			title.remove(t)
	para=soup.find_all("div",{"class":"b_caption"})
	paras=[]
	for p in para:
		#print p
		#print "\n"
		paras.append(p.find('p').getText())
	titles=[]
	links = []
	for t in title[:]:
		a = t.find('a',href=True)
		titles.append(t.getText())
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
	cursor.execute("DROP TABLE IF EXISTS bing")

	# Create table as per requirement
	sql = """CREATE TABLE bing
	(
	ID int NOT NULL AUTO_INCREMENT,
	title text NOT NULL,
	link text,
	description text,
	PRIMARY KEY (ID)
	)"""

	cursor.execute(sql)
	br=0
	for t,l,p in zip(titles,links,paras):
		# Prepare SQL query to INSERT a record into the database.
		#sql = "INSERT INTO yahoo \
		#	(TITLE, LINK, DESC) \
		#	VALUES ('%s', '%s', '%s')" % (t,l,p)
		if(len(l)>150):
			continue
		query = "INSERT INTO bing(title,link,description) VALUES(%s,%s,%s)"
		args = (t.encode('utf8'), l.encode('utf8'), p.encode('utf8'))
		try:
		   # Execute the SQL command
		   print "executing"
		   cursor.execute(query, args)
		   print "inserted a row!"
		   # Commit your changes in the database
		   db.commit()
		except:
		   # Rollback in case there is any error
		   print "failed"
		   db.rollback()
		   #db.commit()
	#	br = br+1
	#	if br == 10:
	#		break

	# disconnect from server
	db.close()
