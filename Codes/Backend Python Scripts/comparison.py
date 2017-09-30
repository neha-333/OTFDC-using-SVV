#!/usr/bin/python
import urllib2
import MySQLdb
from bs4 import BeautifulSoup

def insert_db(table,cursor,search_engine,db):
	query = """SELECT * FROM %s """ % search_engine
	cursor.execute(query)
	search_results = cursor.fetchall()
	for row in search_results:
		title = row[1]
		link_1 = row[2]
		description = row[3]
		#print row
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

		link_exists_query = "SELECT * FROM %s WHERE link = '%s' OR link = '%s' OR link = '%s' " % (table,link_1,link_2,link_3)
		cursor.execute(link_exists_query)
		link_exists = cursor.fetchall()
		get_rank = "SELECT id FROM %s WHERE link IN ('%s','%s','%s') " % (search_engine,link_1,link_2,link_3)
		cursor.execute(get_rank)
		rank = cursor.fetchall()
		if len(link_exists) == 0:
			if table=="result":
				insert_query = "INSERT INTO result (title,link,description,ranky,rankb,rankaol,rankask) VALUES (%s,%s,%s,%s,%s,%s,%s)"
			if table=="a":
				insert_query = "INSERT INTO a (title,link,description,ranky,rankb,rankaol,rankask) VALUES (%s,%s,%s,%s,%s,%s,%s)"
			if table=="b":
				insert_query = "INSERT INTO b (title,link,description,ranky,rankb,rankaol,rankask) VALUES (%s,%s,%s,%s,%s,%s,%s)"
			if table=="c":
				insert_query = "INSERT INTO c (title,link,description,ranky,rankb,rankaol,rankask) VALUES (%s,%s,%s,%s,%s,%s,%s)"
			if table=="d":
				insert_query = "INSERT INTO d (title,link,description,ranky,rankb,rankaol,rankask) VALUES (%s,%s,%s,%s,%s,%s,%s)"
			if table=="e":
				insert_query = "INSERT INTO e (title,link,description,ranky,rankb,rankaol,rankask) VALUES (%s,%s,%s,%s,%s,%s,%s)"
						
			if search_engine == "yahoo":
				insert_args = (title,link_1,description,rank[0][0],int(0),int(0),int(0))
			elif search_engine == "bing":
				insert_args = (title,link_1,description,int(0),rank[0][0],int(0),int(0))
			elif search_engine == "aol":
				insert_args = (title,link_1,description,int(0),int(0),rank[0][0],int(0))
			elif search_engine == "ask":
				insert_args = (title,link_1,description,int(0),int(0),int(0),rank[0][0])
			try:
				cursor.execute(insert_query,insert_args)
				db.commit()
				print "inserted in result!"
			except:
				print "failed in result"
				db.rollback()
		else:
			if search_engine == "yahoo":
				arg_search = "ranky"
			elif search_engine == "bing":
				arg_search = "rankb"
			elif search_engine == "ask":
				arg_search = "rankask"
			elif search_engine == "aol":
				arg_search = "rankaol"

			update_query = "UPDATE %s SET %s = %s WHERE link IN ('%s','%s','%s')" % \
					(table,arg_search,rank[0][0],link_1,link_2,link_3)

			try:
				cursor.execute(update_query)
				db.commit()
				print "updated!"
			except:
				print "failed"
				db.rollback()


def calc_weights(table,cursor,db):
	ayahoo = 0.895
	abing = 0.845
	aask = 0.680
	aaol = 0.580
	suma = ayahoo + abing + aask + aaol
	beta = -0.5
	get_ranks_query = "SELECT id,ranky,rankb,rankaol,rankask from %s" %table
	cursor.execute(get_ranks_query)
	ranks = cursor.fetchall()
	for row in ranks:
		idd = row[0]
		ranky = row[1]
		rankb = row[2]
		rankask = row[3]
		rankaol = row[4]
		weightc = 0
		if(ranky != 0):
			weightc = weightc + ayahoo*(ranky**beta)
		if(rankb != 0):
                	weightc = weightc + abing*(rankb**beta)
		if(rankask != 0):
			weightc = weightc + aask*(rankask**beta)
		if(rankaol != 0):
			weightc = weightc + aaol*(rankaol**beta);
		votec = weightc/suma
		update_query = "UPDATE %s SET weight = %s, vote_distr = %s WHERE id = %s" % (table,float(weightc),float(votec),int(idd))
		cursor.execute(update_query)
		db.commit()

	avg_weight_query = "SELECT AVG(weight), STDDEV(weight), count(*) FROM %s" %table
	cursor.execute(avg_weight_query)
	weight = cursor.fetchall()
	avg_weight = weight[0][0]
	std_dev = weight[0][1]
	print weight[0][0]
	print weight[0][1]
	n  = 2
	thresh = avg_weight + n*std_dev
	print avg_weight, std_dev, n, thresh
	get_weights = "SELECT id, weight FROM %s" %table
	cursor.execute(get_weights)
	weight_results = cursor.fetchall()

	for row in weight_results:
		idd = row[0]
		w = row[1]
		if(w > thresh):
			rel = 1
		elif(w < thresh and w > avg_weight):
			rel = 0.5
		else:
			rel = 0
		update_query = "UPDATE %s SET relevance = %s WHERE id = %s" % (table,float(rel),int(idd))
		cursor.execute(update_query)
		db.commit()
