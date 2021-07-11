######################################################
##  File:           query_links.py
##  Description:    List of links the sql service uses to retrieve the data from the api
##  Author:         Emmanuel Ojo
##  Date:           July 11 2021
##  Last Updated:   
######################################################  

from api_key import *

class queryAPILinks():

    # api url/key object
    tmdbAPI = keys()

    ########################################
    # Title: getUpcomingMoviesLink
    #
    # Description: Gets the upcoming movies data
    #
    # Details:
    #       - https://api.themoviedb.org/3/movie/upcoming
    #
    #########

    def getUpcomingMoviesLink(self):
        upcomingMoviesLink = "https://api.themoviedb.org/3/movie/upcoming" + self.tmdbAPI.getAPIKey() + "&language=en-US&page="
        return upcomingMoviesLink


    ########################################
    # Title: getNowPlayingMoviesLink
    #
    # Description: Gets the now playing movies data
    #
    # Details:
    #       - https://api.themoviedb.org/3/movie/now_playing
    #
    #########

    def getNowPlayingMoviesLink(self):
        nowPlayingMoviesLink = "https://api.themoviedb.org/3/movie/now_playing" + self.tmdbAPI.getAPIKey() + "&language=en-US&page="
        return nowPlayingMoviesLink


    ########################################
    # Title: getPopularMoviesLink
    #
    # Description: Gets the popular movies data
    #
    # Details:
    #       - https://api.themoviedb.org/3/movie/popular
    #
    #########

    def getPopularMoviesLink(self):
        popularMoviesLink = "https://api.themoviedb.org/3/movie/popular" + self.tmdbAPI.getAPIKey() + "&language=en-US&page="
        return popularMoviesLink


    ########################################
    # Title: getTopRatedMoviesLink
    #
    # Description: Gets the top rated movies data
    #
    # Details:
    #       - https://api.themoviedb.org/3/movie/top_rated
    #
    #########

    def getTopRatedMoviesLink(self):
        topRatedMoviesLink = "https://api.themoviedb.org/3/movie/top_rated" + self.tmdbAPI.getAPIKey() + "&language=en-US&page="
        return topRatedMoviesLink

    ########################################
    # Title: getTrendingMoviesTodayLink
    #
    # Description: Gets the trending today movies data
    #
    # Details:
    #       - https://api.themoviedb.org/3/trending/movie/day
    #
    #########

    def getTrendingMoviesTodayLink(self):
        trendingMoviesTodayLink = "https://api.themoviedb.org/3/trending/movie/day" + self.tmdbAPI.getAPIKey() + "&language=en-US&page="
        return trendingMoviesTodayLink

    ########################################
    # Title: getTrendingMoviesWeeklyLink
    #
    # Description: Gets the trending weekly movies data
    #
    # Details:
    #       - https://api.themoviedb.org/3/trending/movie/week
    #
    #########

    def getTrendingMoviesWeeklyLink(self):
        trendingMoviesWeeklyLink = "https://api.themoviedb.org/3/trending/movie/week" + self.tmdbAPI.getAPIKey() + "&language=en-US&page="
        return trendingMoviesWeeklyLink


    ########################################
    # Title: getPopularTVShowsLink
    #
    # Description: Gets the popular tv shows data
    #
    # Details:
    #       - https://api.themoviedb.org/3/tv/popular
    #
    #########

    def getPopularTVShowsLink(self):
        popularTVShowsLink = "https://api.themoviedb.org/3/tv/popular" + self.tmdbAPI.getAPIKey() + "&language=en-US&page="
        return popularTVShowsLink


    ########################################
    # Title: getTopRatedTVShowsLink
    #
    # Description: Gets the top rated tv shows data
    #
    # Details:
    #       - https://api.themoviedb.org/3/tv/top_rated
    #
    #########

    def getTopRatedTVShowsLink(self):
        topRatedTVShowsLink = "https://api.themoviedb.org/3/tv/top_rated" + self.tmdbAPI.getAPIKey() + "&language=en-US&page="
        return topRatedTVShowsLink


    ########################################
    # Title: getTrendingTVShowsTodayLink
    #
    # Description: Gets the trending today tv shows data
    #
    # Details:
    #       - https://api.themoviedb.org/3/trending/tv/day
    #
    #########

    def getTrendingTVShowsTodayLink(self):
        trendingTVShowsTodayLink = "https://api.themoviedb.org/3/trending/tv/day" + self.tmdbAPI.getAPIKey() + "&language=en-US&page="
        return trendingTVShowsTodayLink


    ########################################
    # Title: getTrendingTVShowsWeeklyLink
    #
    # Description: Gets the trending weekly tv shows data
    #
    # Details:
    #       - https://api.themoviedb.org/3/trending/tv/week
    #
    #########

    def getTrendingTVShowsWeeklyLink(self):
        trendingTVShowsWeeklyLink = "https://api.themoviedb.org/3/trending/tv/week" + self.tmdbAPI.getAPIKey() + "&language=en-US&page="
        return trendingTVShowsWeeklyLink


    ########################################
    # Title: getTrendingAllTodayLink
    #
    # Description: Gets the trending today ALL data
    #
    # Details:
    #       - https://api.themoviedb.org/3/trending/all/day
    #
    #########

    def getTrendingAllTodayLink(self):
        trendingAllTodayLink = "https://api.themoviedb.org/3/trending/all/day" + self.tmdbAPI.getAPIKey() + "&language=en-US&page="
        return trendingAllTodayLink


    ########################################
    # Title: getTrendingAllWeeklyLink
    #
    # Description: Gets the trending weekly ALL data
    #
    # Details:
    #       - https://api.themoviedb.org/3/trending/all/week
    #
    #########

    def getTrendingAllWeeklyLink(self):
        trendingAllWeeklyLink = "https://api.themoviedb.org/3/trending/all/week" + self.tmdbAPI.getAPIKey() + "&language=en-US&page="
        return trendingAllWeeklyLink