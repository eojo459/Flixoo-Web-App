######################################################
##  File:           movie_queries.py
##  Description:    Get all the queries related to the movies page
##  Author:         Emmanuel Ojo
##  Date:           December 17 2020
##  Last Updated:   July 10 2021
######################################################

from sql_table_select import *

## July 10 2021 UPDATE: pages now query the sql databases instead of using the api query each time

class moviePageQueries:

    ########################################
    # Title: showAllMoviesPage
    #
    # Description: Gets all the data from the SQL DATABASE that relates to anything MOVIES
    #
    # Details:
    #       - UPCOMING MOVIES GET REQUEST LINK = https://api.themoviedb.org/3/movie/upcoming?api_key=<<apikey>>&language=en-US&page=1
    #       - NOW PLAYING MOVIES GET REQUEST LINK = https://api.themoviedb.org/3/movie/now_playing?api_key=<<apikey>>&language=en-US&page=1
    #       - POPULAR MOVIES GET REQUEST LINK = https://api.themoviedb.org/3/movie/popular?api_key=<<apikey>>&language=en-US&page=1
    #       - TOP RATED MOVIES GET REQUEST LINK = https://api.themoviedb.org/3/movie/top_rated?api_key=<<apikey>>&language=en-US&page=1
    #       - TRENDING MOVIES TODAY GET REQUEST LINK = https://api.themoviedb.org/3/trending/movie/day?api_key=<<apikey>>
    #       - TRENDING MOVIES WEEKLY GET REQUEST LINK = https://api.themoviedb.org/3/trending/movie/week?api_key=<<apikey>>
    #       - returns the completed dictionaries for upcomingMovies, nowPlayingMovies, popularMovies, topRatedMovies, trendingTodayMovies and trendingWeeklyMovies
    #       - this is where the site gets its local data for the titles, posters, descriptions etc for anything MOVIES related
    #
    #########
    def showAllMoviePage(self):

        # sql table names
        upcomingMoviesTable = 'upcoming-Movies'
        nowPlayingMoviesTable = 'now-Playing-Movies'
        popularMoviesTable = 'popular-Movies'
        topRatedMoviesTable = 'top-Rated-Movies'
        trendingTodayMoviesTable = 'trending-Today-Movies'
        trendingWeeklyMoviesTable = 'trending-Weekly-Movies'

        # sql table select object
        tableSelect = sqlSelect()

        # select data from sql tables
        try:
            print("--- Loading data for movies page ---")

            self.upcomingMovies = tableSelect.selectFromTable(upcomingMoviesTable)
            print("Upcoming movies loaded!")

            self.nowPlayingMovies = tableSelect.selectFromTable(nowPlayingMoviesTable)
            print("Now playing movies loaded!")

            self.popularMovies = tableSelect.selectFromTable(popularMoviesTable)
            print("Popular movies loaded!")

            self.topRatedMovies = tableSelect.selectFromTable(topRatedMoviesTable)
            print("Top rated movies loaded!")

            self.trendingTodayMovies = tableSelect.selectFromTable(trendingTodayMoviesTable)
            print("Trending today movies loaded!")

            self.trendingWeeklyMovies = tableSelect.selectFromTable(trendingWeeklyMoviesTable)
            print("Trending weekly movies loaded!")

            # return results
            return self.trendingTodayMovies, self.trendingWeeklyMovies, self.upcomingMovies, self.nowPlayingMovies, self.popularMovies, self.topRatedMovies
        except:
            print("Error getting new data from the database for Movies")