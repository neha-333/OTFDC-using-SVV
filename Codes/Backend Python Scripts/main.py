#!/usr/bin/python
import urllib2
import MySQLdb
from bs4 import BeautifulSoup
import aol
import ask
import sys
import scrapy
import scrapyyahoo
import comparison
from multiprocessing import Pool

def svv(q):

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
	cursor.execute("DROP TABLE IF EXISTS result")

	# Create table as per requirement
	sql = """CREATE TABLE result
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
	)"""

	cursor.execute(sql)

	comparison.insert_db("result",cursor,"yahoo",db)
	comparison.insert_db("result",cursor,"aol",db)
	comparison.insert_db("result",cursor,"ask",db)
	comparison.insert_db("result",cursor,"bing",db)

	comparison.calc_weights("result",cursor,db)
	# disconnect from server
	db.close()

if __name__ == "__main__":
   svv(sys.argv[1])
