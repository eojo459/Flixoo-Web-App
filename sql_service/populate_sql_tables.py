######################################################
##  File:           populate_sql_tables.py
##  Description:    Populated each sql table with the data retrieved from the api queries
##  Author:         Emmanuel Ojo
##  Date:           July 11 2021
##  Last Updated:   
###################################################### 

from .mysql_connection import *


class populateTables():

    ########################################
    # Title: updateSQLTable
    #
    # Description: Updates each sql table with new information if there are any
    #
    # Details:
    #       - REPLACE INTO { table name }
    #         SET Content_ID = { id }, Ranking = { ranking }, Content_Type = { type }, Movie_Title = { title }
    #             Overview = { overview }, Poster = { poster }, Release_Date = { release }, Rating = { rating }, 
    #             Genres = { genres }, Trailer = { trailer }, Providers = { providers }        
    #
    #       - Replaces old data with new data if there is anything to overwrite, else creates new item
    #       - Cleans up tables by deleting any items that were not recently inserted/updated as they are now irrelevant
    #
    #########

    def updateSQLTable(self, records, tableName):

        print("Updating table " + tableName + "..")

        # connect to database
        db = mySQLConnection().createConnection()

        # cursor
        cursor = db.cursor()

        # keep track of items we updated, do not clean them
        updatedIDList = []

        # update each record in the table, if it does not exist create it, else update it
        for record in records:
            
            query = '''
                    REPLACE INTO `%s`
                    SET Content_ID = '%s', Ranking = '%s', Content_Type = '%s', Movie_Title = %s, 
                        Overview = %s, Poster = '%s', Release_Date = '%s', Rating = '%s', 
                        Genres = '%s', Trailer = '%s', Providers = %s
            ''' % (tableName, record[0], record[1], record[2], repr(record[3]), repr(record[4]), record[5], record[6], record[7], record[8], record[9], repr(record[10]))
            
            updatedIDList.append(record[0]) # add id to updated list

            cursor.execute(query)

        # commit
        db.commit()

        updatedIDTuple = tuple(updatedIDList)
        
        # clean up table, delete items that were not recently inserted/updated -> delete items not in the updatedIDTuple
        print("Cleaning up " + tableName + "..")

        query = '''
                DELETE FROM `%s`
                WHERE Content_ID NOT IN %s
        ''' % (tableName, str(updatedIDTuple))

        cursor.execute(query)

        # commit
        db.commit()
        
        db.close()

