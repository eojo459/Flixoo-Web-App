######################################################
##  File:           movie_queries.py
##  Description:    Get all the queries related to the movies page
##  Author:         Emmanuel Ojo
##  Date:           December 17 2020
##  Last Updated:   January 2 2021
######################################################

import requests
import json
from api_key import *
from query_tools import *

class moviePageQueries:

    # store poster links for each popularity subject
    upcomingMovies = {}
    nowPlayingMovies = {}
    popularMovies = {}
    topRatedMovies = {}
    trendingTodayMovies = {}
    trendingWeeklyMovies = {}


    ########################################
    # Title: showAllMoviesPage
    #
    # Description: Gets all the data from the API that relates to anything MOVIES
    #
    # Details:
    #       - UPCOMING MOVIES GET REQUEST LINK = https://api.themoviedb.org/3/movie/upcoming?api_key=<<apikey>>&language=en-US&page=1
    #       - NOW PLAYING MOVIES GET REQUEST LINK = https://api.themoviedb.org/3/movie/now_playing?api_key=<<apikey>>&language=en-US&page=1
    #       - POPULAR MOVIES GET REQUEST LINK = https://api.themoviedb.org/3/movie/popular?api_key=<<apikey>>&language=en-US&page=1
    #       - TOP RATED MOVIES GET REQUEST LINK = https://api.themoviedb.org/3/movie/top_rated?api_key=<<apikey>>&language=en-US&page=1
    #       - TRENDING MOVIES TODAY GET REQUEST LINK = https://api.themoviedb.org/3/trending/movie/day?api_key=<<apikey>>
    #       - TRENDING MOVIES WEEKLY GET REQUEST LINK = https://api.themoviedb.org/3/trending/movie/week?api_key=<<apikey>>
    #       - returns the completed dictionaries for upcomingMovies, nowPlayingMovies, popularMovies, topRatedMovies, trendingTodayMovies and trendingWeeklyMovies
    #       - this is where the site gets it local data for the titles, posters, descriptions etc for anything MOVIES related
    #
    #########
    def showAllMoviePage(self):
        
        # api requests
        tmdbAPI = keys()

        # split url links
        trendingMoviesTodayLink = [tmdbAPI.getAPIUrl(), '/trending', '/movie', '/day', tmdbAPI.getAPIKey()]
        trendingMoviesWeeklyLink = [tmdbAPI.getAPIUrl(), '/trending', '/movie', '/week', tmdbAPI.getAPIKey()]
        upcomingMoviesLink = [tmdbAPI.getAPIUrl(), '/movie', '/upcoming', tmdbAPI.getAPIKey()]
        nowPlayingMoviesLink = [tmdbAPI.getAPIUrl(), '/movie', '/now_playing', tmdbAPI.getAPIKey()]
        popularMoviesLink = [tmdbAPI.getAPIUrl(), '/movie', '/popular', tmdbAPI.getAPIKey()]
        topRatedMoviesLink = [tmdbAPI.getAPIUrl(), '/movie', '/top_rated', tmdbAPI.getAPIKey()]

        # get data from all the pages we need
        pages = 5
        print("########################## MOVIES PAGE ##########################")
        showAllMovies = queryFunctionTools()
        showAllMovies.showAll(trendingMoviesTodayLink, self.trendingTodayMovies, pages)
        showAllMovies.showAll(trendingMoviesWeeklyLink, self.trendingWeeklyMovies, pages)
        showAllMovies.showAll(upcomingMoviesLink, self.upcomingMovies, pages)
        showAllMovies.showAll(nowPlayingMoviesLink, self.nowPlayingMovies, pages)
        showAllMovies.showAll(popularMoviesLink, self.popularMovies, pages)
        showAllMovies.showAll(topRatedMoviesLink, self.topRatedMovies, pages)

        # return array of poster image urls
        return self.trendingTodayMovies, self.trendingWeeklyMovies, self.upcomingMovies, 
        self.nowPlayingMovies, self.popularMovies, self.topRatedMovies