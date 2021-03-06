#designed to convert all the json CU event data provided by IARPA (in the cu_gsr data)
#into a sql database for use later.  will try to format dates into 
#sql datetime format for easy time-based queries.

#created by Austin Peterson

import json
import sqlite3
import time
import os

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def execute_sql_comm(conn, sql_comm):
    try:
        c = conn.cursor()
        c.execute(sql_comm)
    except Error as e:
        print(e)

def main():

	database = "cu_gsr.db"
	#replace this if you're not austin
	path = '/Users/austinpeterson/Documents/code/MercuryChallenge/jsonToSql/cu_gsr/'

	counter = 0
	#read each json file included in cu_gsr
	for filename in os.listdir(path):

		temppath = path+filename

		with open(temppath, "r") as read_file:
			data = json.load(read_file)

		print("===========================Now reading "+filename+"===========================")

		sql_create_cu_gsr_event_table = """CREATE TABLE IF NOT EXISTS cu_gsr_event (
                                        Approximate_Location text,
                                        City text,
                                        Country text,
                                        Crowd_Size,
                                        Crowd_Size_Description text,
                                        Earliest_Reported_Date text,
                                        Encoding_Comment text,
                                        Event_Date datetime,
                                        Event_ID text,
                                        Event_Type text,
                                        First_Reported_Link text,
                                        GSS_Link text,
                                        Latitude text,
                                        Longitude text,
                                        News_Source text,
                                        Other_Links text,
                                        Population text,
                                        Reason text,
                                        Revision_Date datetime,
                                        State text
                                );"""

		# create a database connection
		conn = create_connection(database)
		if conn is not None:
			# create projects table
			execute_sql_comm(conn, sql_create_cu_gsr_event_table)
		else:
			print("cannot create db connection.")

		c = conn.cursor()

		#parse json data into vars
		for entry in data:
			try:
				query = '(Approximate_Location, City, Country, Crowd_Size, Crowd_Size_Description,Earliest_Reported_Date,Encoding_Comment,Event_Date,Event_ID,Event_Type, \
				First_Reported_Link,GSS_Link,Latitude,Longitude,News_Source,Other_Links,Population,Reason,Revision_Date,State)'

				c.execute('INSERT INTO cu_gsr_event ' + query + ' VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', \
				(entry['Approximate_Location'],entry['City'], entry['Country'], entry['Crowd_Size'], entry['Crowd_Size_Description'], \
				entry['Earliest_Reported_Date'],entry['Encoding_Comment'], entry['Event_Date'], entry['Event_ID'], entry['Event_Type'], \
				entry['First_Reported_Link'],entry['GSS_Link'], entry['Latitude'], entry['Longitude'], entry['News_Source'], \
				entry['Other_Links'],entry['Population'], entry['Reason'], entry['Revision_Date'], entry['State']))

				print("Event: "+entry['Event_ID']+" inserted into "+database)
			except Error as e:
				print(entry['Event_ID']+" not successful. Error: "+e)
			
			#make sure entry as datetime works in db

		conn.commit()
		counter = counter+1
	print(str(counter)+" json files read from "+path)

main()







	
