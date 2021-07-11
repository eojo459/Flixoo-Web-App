######################################################
##  File:           sql_service_start.py
##  Description:    Start the sql update database service (~7 minutes to run fully)
##  Author:         Emmanuel Ojo
##  Date:           July 11 2021
##  Last Updated:   
######################################################  

from .mysql_connection import *
from .create_sql_tables import *
from .populate_sql_tables import *
from .query_api import *
from .sql_table_select import *
import traceback



class sqlService:

    ########################################
    # Title: sqlServiceMain
    #
    # Description: Main function for sql service, it updates the SQL database
    #
    # Details:
    #       - Runs all the api queries and stores the data in the sql database if there are any updates
    #
    #########

    def sqlServiceMain(self):

        # test connection to mySQL DB
        print("########## CONNECT TO DATABASE ##########")
        print("Connecting to host server..")
        try:
            dbConnection = mySQLConnection().createConnection()
            print("Successfully connected to host server")
        except:
            print("**Error connecting to host server - Terminating Program")
            traceback.print_exc()
            return

        # create tables if needed
        print("########## CREATE DATABASE TABLES ##########")
        tables = createTables().createTables()

        # get data and insert/populate tables
        updateDB = True
        print("########## GET DATA AND INSERT INTO DATABASE ##########")
        apiQuery = queryResult().queryResultMain(updateDB)


'''
if __name__ == "__main__":
    main()
'''
