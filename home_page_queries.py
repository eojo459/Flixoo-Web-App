######################################################
##  File:           home_page_queries.py
##  Description:    Get all the queries related to the homepage
##  Author:         Emmanuel Ojo
##  Date:           December 17 2020
##  Last Updated:   January 2 2021
######################################################   

import requests
import json
from api_key import *
from query_tools import *
from movies_queries import *
from tv_queries import *


class homePageQueryLinks():

    # dictionary with api data, used for local database
    trendingToday = {}
    trendingWeekly = {}

    ########################################
    # Title: showAllHomePage
    #
    # Description: Gets all the data from the API that relates to anything TRENDING
    #
    # Details:
    #       - GET ALL TRENDING TODAY CONTENT API GET LINK = https://api.themoviedb.org/3/trending/all/day?api_key=<<apikey>>
    #       - GET ALL TRENDING WEEKLY CONTENT API GET LINK = https://api.themoviedb.org/3/trending/all/week?api_key=<<apikey>>
    #       - returns the completed dictionaries for trendingToday and trendingWeekly
    #       - this is where the site gets it local data for the titles, posters, descriptions etc for anything trending related
    #
    #########
    def showAllHomePage(self):
        
        # api requests
        tmdbAPI = keys()

        # split url link
        trendingTodayLink = [tmdbAPI.getAPIUrl(), '/trending', '/all', '/day', tmdbAPI.getAPIKey()]
        trendingWeeklyLink = [tmdbAPI.getAPIUrl(), '/trending', '/all', '/week', tmdbAPI.getAPIKey()]
        
        # get data from all the pages we need
        pages = 5
        print("########################## ALL TRENDING PAGE ##########################")
        showAllTrendingData = queryFunctionTools()
        showAllTrendingData.showAll(trendingTodayLink, self.trendingToday, pages)
        showAllTrendingData.showAll(trendingWeeklyLink, self.trendingWeekly, pages)
        
        # return arrays with info
        return self.trendingToday, self.trendingWeekly
