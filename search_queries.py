######################################################
##  File:           search_queries.py
##  Description:    Returns the results from the search query
##  Author:         Emmanuel Ojo
##  Date:           January 7 2021
##  Last Updated:   
######################################################   

import requests
import json
from api_key import *
from query_tools import *


class searchQueryLinks():

    # dictionary with api data, used for local database
    searchResults = {}

    ########################################
    # Title: showAllSearchResults
    #
    # Description: Gets all the data from the API that relates to the search query
    #
    # Details:
    #       - SEARCH QUERY API GET LINK =  https://api.themoviedb.org/3/search/multi?api_key=<<apikey>>&language=en-US&query=<<searchQuery>>&page=1&include_adult=false
    #       - returns the completed dictionaries for searchResults
    #       - this is where the site gets it local data for the titles, posters, descriptions etc for the search results
    #
    #########
    def showAllSearchResults(self, searchQuery):

        # clear data from previous results
        self.searchResults = {}
        
        if searchQuery == "":
            return

        # api requests
        tmdbAPI = keys()

        # split url link
        multiSearchLink = [tmdbAPI.getAPIUrl(), '/search', '/multi', tmdbAPI.getAPIKey(), '&query=', searchQuery]
        
        # get data from all the pages we need
        pages = 1
        print("########################## ALL SEARCH RESULTS ##########################")
        showAllSearch = queryFunctionTools()
        showAllSearch.showAll(multiSearchLink, self.searchResults, pages)
        
        # return arrays with info
        return self.searchResults

    ########################################
    # Title: searchCount
    #
    # Description: Count the amount of results we have in the dictionary
    #
    # Details:
    #       - checks each index in the dictionary and returns the count for the total dictionary
    #
    #########
    def searchCount(self):
        count = 0

        for index in self.searchResults:
            count += 1
        
        return count
