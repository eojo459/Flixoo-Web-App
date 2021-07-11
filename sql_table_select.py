######################################################
##  File:           sql_table_select.py
##  Description:    Query the sql database and select the data
##  Author:         Emmanuel Ojo
##  Date:           July 10 2021
##  Last Updated:   
######################################################

from mysql_connection import *

class sqlSelect():

    ########################################
    # Title: selectFromTable
    #
    # Description: Gets all the data from the sql databases
    #
    # Details:
    #       - "SELECT * FROM {tableName} ORDER BY Ranking ASC" -> select everything starting from the most popular (1,2,3... etc)
    #       - stores data in a list of dictionaries which are accessed by the html code to display their contents
    #
    #########
    def selectFromTable(self, tableName):

        # connect to database
        db = mySQLConnection().createConnection()

        # cursor
        cursor = db.cursor()

        # select everything from the given table name, sorted by ranking (ascending)
        #print("Selecting from table " + tableName)
        query = "SELECT * FROM `%s` ORDER BY Ranking ASC" % (tableName)

        cursor.execute(query)

        # save results
        sqlResult = cursor.fetchall()
        
        #array for results
        sqlResultList = []

        for item in sqlResult:
            sqlResultList.append(
                {
                    'Content_ID': str(item[0]),
                    'Ranking': str(item[1]),
                    'Content_Type':str(item[2]),
                    'Title': str(item[3]),
                    'Overview': str(item[4]),
                    'Poster_URL': str(item[5]),
                    'Release_Date': str(item[6]),
                    'Rating': str(item[7]),
                    'Genres': str(item[8]),
                    'Trailer': str(item[9]),
                    'Providers': str(item[10])
                }
            )

        db.close()

        return sqlResultList