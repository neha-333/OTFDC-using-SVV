
import urllib2
import MySQLdb
from bs4 import BeautifulSoup
def getreverse(query):
	req = urllib2.Request("http://www.ask.com/web?q="+query,headers={'User-Agent':"Google Chrome"})
	con=urllib2.urlopen(req)
	content = con.read()
	soup = BeautifulSoup(content)
	related=soup.find_all("a",{"class":"related-search-item-link"})
	relateds=[]
	for r in related:
		relateds.append(r.getText())
		print r.getText()
	print len(relateds)
	# Open database connection
	db = MySQLdb.connect(db='svvtest', user='root', passwd='', unix_socket="/opt/lampp/var/mysql/mysql.sock")
	# prepare a cursor object using cursor() method
	cursor = db.cursor()
	# Drop table if it already exist using execute() method.
	cursor.execute("DROP TABLE IF EXISTS reverselink")

	# Create table as per requirement
	sql = """CREATE TABLE reverselink
	(
	ID int NOT NULL AUTO_INCREMENT,
	related text NOT NULL,
	PRIMARY KEY (ID)
	)"""

	cursor.execute(sql)

	for r in relateds:	
		# Prepare SQL query to INSERT a record into the database.
		#sql = "INSERT INTO ask \
		#	(TITLE, LINK, DESC) \
		#	VALUES ('%s', '%s', '%s')" % (t,l,p)
		query = "INSERT INTO reverselink(related) " \
		    "VALUES(%s)"
		args = (r.encode('utf8'))
		try:
		   # Execute the SQL command
		   cursor.execute(query, args)
		   # Commit your changes in the database
		   print "inserted a row!"
		   db.commit()
		except:
		   # Rollback in case there is any error
		   print "failed"
		   db.rollback()

	# disconnect from server
	
	db.close()
	return relateds

