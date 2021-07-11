######################################################
##  File:           tv_queries.py
##  Description:    Get all the queries related to the TV page
##  Author:         Emmanuel Ojo
##  Date:           December 17 2020
##  Last Updated:   July 10 2021
######################################################

from sql_table_select import *

## July 10 2021 UPDATE: pages now query the sql databases instead of using the api query each time

class tvPageQueries:

    ########################################
    # Title: showAllTVPage
    #
    # Description: Gets all the data from the SQL DATABASE that relates to anything TV SHOWS
    #
    # Details:
    #       - TRENDING TV SHOWS TODAY GET API LINK = https://api.themoviedb.org/3/trending/tv/day?api_key=<<apikey>>
    #       - TRENDING TV SHOWS WEEKLY GET REQUEST LINK= https://api.themoviedb.org/3/trending/tv/week?api_key=<<apikey>>
    #       - POPULAR TV SHOWS GET REQUEST LINK = https://api.themoviedb.org/3/tv/popular?api_key=<<apikey>>&language=en-US&page=1
    #       - TOP RATED TV SHOWS GET REQUEST LINK = https://api.themoviedb.org/3/tv/top_rated?api_key=<<apikey>>&language=en-US&page=1
    #       - returns the completed dictionaries for popularTV, topRatedTV, trendingTodayTV and trendingWeeklyTV
    #       - this is where the site gets its local data for the titles, posters, descriptions etc for anything TV SHOW related
    #
    #########
    def showAllTVPage(self):
        
        # sql table names
        popularTVTable = 'popular-TV-Shows'
        topRatedTVTable = 'top-Rated-TV-Shows'
        trendingTodayTVTable = 'trending-Today-TV-Shows'
        trendingWeeklyTVTable = 'trending-Weekly-TV-Shows'

        # sql table select object
        tableSelect = sqlSelect()

        # select data from sql tables
        try:
            print("--- Loading data for tv shows page ---")

            self.popularTV = tableSelect.selectFromTable(popularTVTable)
            print("Popular tv loaded!")

            self.topRatedTV = tableSelect.selectFromTable(topRatedTVTable)
            print("Top rated tv loaded!")

            self.trendingTodayTV = tableSelect.selectFromTable(trendingTodayTVTable)
            print("Trending today tv loaded!")

            self.trendingWeeklyTV = tableSelect.selectFromTable(trendingWeeklyTVTable)
            print("Trending weekly tv loaded!")

            # return results
            return self.popularTV, self.topRatedTV, self.trendingTodayTV, self.trendingWeeklyTV
        except:
            print("Error getting new data from the database for TV Shows")
