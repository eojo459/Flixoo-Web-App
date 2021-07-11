######################################################
##  File:           create_sql_tables.py
##  Description:    Creates sql tables if they dont already exist
##  Author:         Emmanuel Ojo
##  Date:           July 11 2021
##  Last Updated:   
###################################################### 

from .mysql_connection import *


class createTables():

    ########################################
    # Title: createTables
    #
    # Description: Creates new sql tables if they dont exist
    #
    # Details:
    #       - CREATE TABLE IF NOT EXISTS { table name }
    #         (Content_ID INT PRIMARY KEY NOT NULL,
    #           Ranking INT NOT NULL,
    #           Content_Type VARCHAR(7), 
    #           Movie_Title TEXT,
    #           Overview TEXT,
    #           Poster TEXT,
    #           Release_Date VARCHAR(4),
    #           Rating VARCHAR(3),
    #           Genres TEXT,
    #           Trailer TEXT,
    #           Providers TEXT)       
    #
    #
    #########

    def createTables(self):

        # connect to database
        db = mySQLConnection().createConnection()

        # cursor
        cursor = db.cursor()

        # list of all the tables to create
        tableNames = ['ALL-Movies', 'ALL-TV-Shows', 'ALL-Trending-Today', 'ALL-Trending-Weekly','popular-Movies', 
                'popular-TV-Shows', 'top-Rated-Movies', 'top-Rated-TV-Shows', 'trending-Today-Movies',
                'trending-Today-TV-Shows', 'trending-Weekly-Movies', 'trending-Weekly-TV-Shows',
                'upcoming-Movies', 'now-Playing-Movies']
            
        # create a table for each table in tableNames if it does not exist
        for item in tableNames:
            print("Creating table " + item)
            
            query = '''
                    CREATE TABLE IF NOT EXISTS `%s`
                    (Content_ID INT PRIMARY KEY NOT NULL,
                        Ranking INT NOT NULL,
                        Content_Type VARCHAR(7), 
                        Movie_Title TEXT,
                        Overview TEXT,
                        Poster TEXT,
                        Release_Date VARCHAR(4),
                        Rating VARCHAR(3),
                        Genres TEXT,
                        Trailer TEXT,
                        Providers TEXT)
            ''' % (item)

            cursor.execute(query)

        # commit
        db.commit()
        db.close()
