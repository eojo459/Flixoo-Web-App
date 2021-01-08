######################################################
##  File:           tv_queries.py
##  Description:    Get all the queries related to the TV page
##  Author:         Emmanuel Ojo
##  Date:           December 17 2020
##  Last Updated:   January 2 2021
######################################################

import requests
import json
from api_key import *
from query_tools import *

class tvPageQueries:

    # store poster links for each popularity subject
    popularTV = {}
    topRatedTV = {}
    trendingTodayTV = {}
    trendingWeeklyTV = {}


    ########################################
    # Title: showAllTVPage
    #
    # Description: Gets all the data from the API that relates to anything TV SHOWS
    #
    # Details:
    #       - TRENDING TV SHOWS TODAY GET API LINK = https://api.themoviedb.org/3/trending/tv/day?api_key=<<apikey>>
    #       - TRENDING TV SHOWS WEEKLY GET REQUEST LINK= https://api.themoviedb.org/3/trending/tv/week?api_key=<<apikey>>
    #       - POPULAR TV SHOWS GET REQUEST LINK = https://api.themoviedb.org/3/tv/popular?api_key=<<apikey>>&language=en-US&page=1
    #       - TOP RATED TV SHOWS GET REQUEST LINK = https://api.themoviedb.org/3/tv/top_rated?api_key=<<apikey>>&language=en-US&page=1
    #       - returns the completed dictionaries for popularTV, topRatedTV, trendingTodayTV and trendingWeeklyTV
    #       - this is where the site gets it local data for the titles, posters, descriptions etc for anything TV SHOW related
    #
    #########
    def showAllTVPage(self):
        
        # api requests
        tmdbAPI = keys()

        # split url links
        trendingTVTodayLink = [tmdbAPI.getAPIUrl(), '/trending', '/tv', '/day', tmdbAPI.getAPIKey()]
        trendingTVWeeklyLink = [tmdbAPI.getAPIUrl(), '/trending', '/tv', '/week', tmdbAPI.getAPIKey()]
        popularTVLink = [tmdbAPI.getAPIUrl(), '/tv', '/popular', tmdbAPI.getAPIKey()]
        topRatedTVLink = [tmdbAPI.getAPIUrl(), '/tv', '/top_rated', tmdbAPI.getAPIKey()]

        # get data from all the pages we need
        pages = 5
        print("########################## TV PAGE ##########################")
        showAllTV = queryFunctionTools()
        showAllTV.showAll(trendingTVTodayLink, self.trendingTodayTV, pages)
        showAllTV.showAll(trendingTVWeeklyLink, self.trendingWeeklyTV, pages)
        showAllTV.showAll(popularTVLink, self.popularTV, pages)
        showAllTV.showAll(topRatedTVLink, self.topRatedTV, pages)

        # return array of poster image urls
        return self.trendingTodayTV, self.trendingWeeklyTV, self.popularTV, self.topRatedTV
