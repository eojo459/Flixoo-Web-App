######################################################
##  File:           home_page_queries.py
##  Description:    Get all the queries related to the homepage
##  Author:         Emmanuel Ojo
##  Date:           December 17 2020
##  Last Updated:   July 10 2021
######################################################   

from .movies_queries import *
from .tv_queries import *
from sql_service.sql_table_select import *

## July 10 2021 UPDATE: pages now query the sql databases instead of using the api query each time

class homePageQueryLinks():

    ########################################
    # Title: showAllHomePage
    #
    # Description: Gets all the data from the SQL DATABASE that relates to anything TRENDING
    #
    # Details:
    #       - GET ALL TRENDING TODAY CONTENT API GET LINK = https://api.themoviedb.org/3/trending/all/day?api_key=<<apikey>>
    #       - GET ALL TRENDING WEEKLY CONTENT API GET LINK = https://api.themoviedb.org/3/trending/all/week?api_key=<<apikey>>
    #       - returns the completed dictionaries for trendingToday and trendingWeekly
    #       - this is where the site gets its local data for the titles, posters, descriptions etc for anything trending related
    #
    #########
    def showAllHomePage(self):
        
        # sql table names
        trendingTodayALLTable = 'ALL-Trending-Today'
        trendingWeeklyALLTable = 'ALL-Trending-Weekly'

        # sql table select object
        tableSelect = sqlSelect()

        # select data from sql tables
        try:
            print("--- Loading data for home page ---")

            self.trendingToday = tableSelect.selectFromTable(trendingTodayALLTable)
            print("All trending today loaded!")

            self.trendingWeekly = tableSelect.selectFromTable(trendingWeeklyALLTable)
            print("All trending weekly loaded!")

            # return results
            return self.trendingToday, self.trendingWeekly
        except:
            print("Error getting new data from the database for Home Page")

