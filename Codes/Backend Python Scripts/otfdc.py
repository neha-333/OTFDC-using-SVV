#!/usr/bin/python
import urllib2
import MySQLdb
import similar
from bs4 import BeautifulSoup
import main
import aol
import ask
import sys
import scrapy
import scrapyyahoo
import comparison
from multiprocessing import Pool
def svvotfdc(q,c):

	pool = Pool()
	pool.apply_async(aol.aolquery, [q])    # evaluate "solve1(A)" asynchronously
	pool.apply_async(scrapyyahoo.yahooquery, [q])
	pool.apply_async(ask.askquery, [q])
	pool.apply_async(scrapy.bingquery, [q])

	pool.close()
	pool.join()

	# Open database connection
	db = MySQLdb.connect(db='svvtest', user='root', passwd='', unix_socket="/opt/lampp/var/mysql/mysql.sock")

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# Drop table if it already exist using execute() method.
	sql = "DROP TABLE IF EXISTS %s" %c
	cursor.execute(sql)

	# Create table as per requirement
	sql = """CREATE TABLE %s
	(
	ID int NOT NULL AUTO_INCREMENT,
	title text NOT NULL,
	link text,
	description text,
	ranky INTEGER,
	rankb INTEGER,
	rankaol INTEGER,
	rankask INTEGER,
	weight FLOAT,
	vote_distr FLOAT,
	relevance FLOAT,
	PRIMARY KEY (ID)
	)""" %c
	#c=chr(ord(c)+1)
	cursor.execute(sql)

	comparison.insert_db(c,cursor,"yahoo",db)
	comparison.insert_db(c,cursor,"aol",db)
	comparison.insert_db(c,cursor,"ask",db)
	comparison.insert_db(c,cursor,"bing",db)

	comparison.calc_weights(c,cursor,db)
	# disconnect from server
	db.close()

def otfdc_core(q):
	print "hello"
	#q=raw_input("Enter query: ")
	q="%20".join(q.split(" "))

	main.svv(q)

	db = MySQLdb.connect(db='svvtest', user='root', passwd='', unix_socket="/opt/lampp/var/mysql/mysql.sock")

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# Drop table if it already exist using execute() method.
	cursor.execute("SELECT id, vote_distr FROM result ORDER BY weight")

	res = cursor.fetchall()

	reverse = similar.getreverse(q)
	c='a'

	for r in reverse[:5]:
		print "in otfdc"
		r = "%20".join(r.split(" "))
		svvotfdc(r,c)
		c=chr(ord(c)+1)

	sql = "SELECT link, vote_distr from result WHERE vote_distr=(SELECT max(vote_distr) from result)"
	cursor.execute(sql)
	res = cursor.fetchall()

	linkr = res[0][0]
	link_1=linkr
	votemax = res[0][1]
	print linkr, votemax
	ct = "a"
	db.close()

	db = MySQLdb.connect(db='svvtest', user='root', passwd='', unix_socket="/opt/lampp/var/mysql/mysql.sock")

	cursor = db.cursor()

	for c in range(0,5):

		if link_1.find("http") == -1:
				link_2 = "https://"+link_1
				link_3 = "http://"+link_1
		else:
			if link_1.find("https") == -1:
				link_2 = link_1[7:]
				link_3 = "https://"+link_2
			else:
				link_3 = link_1[8:]
				link_2 = "http://"+link_3

		sql = "SELECT vote_distr FROM %s WHERE link = '%s' OR link = '%s' OR link = '%s' " % (ct,link_1,link_2,link_3)
		#sql = "SELECT vote_distr from %s WHERE link='%s'" % (ct,linkr)
	
		cursor.execute(sql)
		res = cursor.fetchall()
		if res:	
			cor_coeff=min(votemax,res[0][0])/votemax
			print cor_coeff,votemax,votemax/3
			if cor_coeff > votemax/3:
				print "Appending" + ct
				sql = "SELECT * FROM %s" %ct
				cursor.execute(sql)
				relres = cursor.fetchall()
				a=0
				for r in relres:
					link_1=relres[a][2]
					if link_1.find("http") == -1:
						link_2 = "https://"+link_1
						link_3 = "http://"+link_1
					else:
						if link_1.find("https") == -1:
							link_2 = link_1[7:]
							link_3 = "https://"+link_2
						else:
							link_3 = link_1[8:]
							link_2 = "http://"+link_3

					link_exists_query = "SELECT * FROM result WHERE link = '%s' OR link = '%s' OR link = '%s' " % (link_1,link_2,link_3)
					cursor.execute(link_exists_query)
					link_exists = cursor.fetchall()
					if len(link_exists) == 0:
						insert_query = "INSERT INTO result (title,link,description,ranky,rankb,rankaol,rankask,weight,vote_distr,relevance) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
						insert_args = (relres[a][1],relres[a][2],relres[a][3],relres[a][4],relres[a][5],relres[a][6],relres[a][7],relres[a][8],relres[a][9],relres[a][10])
						cursor.execute(insert_query,insert_args)
						db.commit()
					a=a+1
		ct=chr(ord(ct)+1)

if __name__ == "__main__":
   otfdc_core(sys.argv[1])
