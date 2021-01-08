import requests
import json
from api_key import *
from query_tools import *
from movies_queries import *
from tv_queries import *

# ALL TRENDING TODAY = https://api.themoviedb.org/3/trending/all/day?api_key=<<apikey>>
# ALL TRENDING WEEKLY = https://api.themoviedb.org/3/trending/all/week?api_key=<<apikey>>
# POPULAR MOVIES = https://api.themoviedb.org/3/movie/popular?api_key=<<apikey>>&language=en-US&page=1
# POPULAR TV SHOWS = https://api.themoviedb.org/3/tv/popular?api_key=<<apikey>>&language=en-US&page=1

class homePageQueryLinks():

    # store poster links for each popularity subject
    allTrendingTodayPosters = []
    allTrendingWeeklyPosters = []
    popularMoviePostersTemp = []
    popularTVPostersTemp = []
    allTrendingTodayTitles = []
    allTrendingWeeklyTitles = []
    allTrendingTodayOverviews = []
    allTrendingWeeklyOverviews = []
    allPopularMovieTitlesTemp = []
    allTrendingTodayRatings = []
    allTrendingWeeklyRatings = []
    allTrendingTodayGenresID = []
    allTrendingTodayGenresName = []
    allTrendingWeeklyGenres = []
    allTrendingTodayTrailers = []


    # SHOW TRENDING MOVIES & TV SHOWS
    # ONLY SHOWS THE FIRST 6
    def trending(self):
        # ALL TRENDING TODAY = https://api.themoviedb.org/3/trending/all/day?api_key=<<apikey>>
        # ALL TRENDING WEEKLY = https://api.themoviedb.org/3/trending/all/week?api_key=<<apikey>>
        
        # api requests
        tmdbLink = keys()
        apiKey = keys()

        # link variables 
        popularity = '/trending'
        content = '/all'
        window1 = '/day'
        window2 = "/week"

        # full link + link variables (TRENDING TODAY)
        allTrendingTodayLink = requests.get(tmdbLink.getAPIUrl() + popularity + content + window1 + apiKey.getAPIKey())        
        posterPathToday = allTrendingTodayLink.json()

        #trendingTodayLink = [tmdbLink.getAPIUrl(), '/trending', '/all', '/day', apiKey.getAPIKey()]

        # full link + link variables (TRENDING WEEKLY)
        allTrendingWeeklyLink = requests.get(tmdbLink.getAPIUrl() + popularity + content + window2 + apiKey.getAPIKey())        
        posterPathWeekly = allTrendingWeeklyLink.json()

        # loop through the json data and find the ['poster_path] values
        # use posterPath() from query_tools.py
        posterPath = queryFunctionTools()

        posterPath.findPosterPath(posterPathToday, self.allTrendingTodayPosters)
        posterPath.findPosterPath(posterPathWeekly, self.allTrendingWeeklyPosters)

        #self.showAllTrending()

        # return array of poster image urls
        return self.allTrendingTodayPosters, self.allTrendingWeeklyPosters


    # SHOW POPULAR MOVIES & TV SHOWS
    # ONLY SHOWS THE FIRST 6
    def popular(self):
        # POPULAR MOVIES = https://api.themoviedb.org/3/movie/popular?api_key=<<apikey>>&language=en-US&page=1
        # POPULAR TV SHOWS = https://api.themoviedb.org/3/tv/popular?api_key=<<apikey>>&language=en-US&page=1
    
        # reuse popularMovies() from movie_queries
        popularMovies = moviePageQueries()

        # reuse popularTV() from tv_queries
        popularTV = tvPageQueries()

        # return array of poster image urls
        self.popularMoviePostersTemp = popularMovies.getPopularMoviePosters()
        self.popularTVPostersTemp = popularTV.getPopularTVPosters()

        return self.popularMoviePostersTemp, self.popularTVPostersTemp


    # SHOW ALL POSTERS FOR TRENDING
    def showAllHomePage(self):
        
        # api requests
        tmdbLink = keys()
        apiKey = keys()

        # split url link
        trendingTodayLink = [tmdbLink.getAPIUrl(), '/trending', '/all', '/day', apiKey.getAPIKey()]
        trendingWeeklyLink = [tmdbLink.getAPIUrl(), '/trending', '/all', '/week', apiKey.getAPIKey()]
        #popularMoviesLink = [tmdbLink.getAPIUrl(), '/movie', '/popular', apiKey.getAPIKey()]
        #trendingMoviesTodayLink = [tmdbLink.getAPIUrl(), '/trending', '/movie', '/day', apiKey.getAPIKey()]

        # get data from all the pages we need
        pages = 2
        showAllTrendingData = queryFunctionTools()
        showAllTrendingData.showAll(trendingTodayLink, self.allTrendingTodayPosters, pages, "poster")
        showAllTrendingData.showAll(trendingWeeklyLink, self.allTrendingWeeklyPosters, pages, "poster")
        showAllTrendingData.showAll(trendingTodayLink, self.allTrendingTodayTitles, pages, "title")
        showAllTrendingData.showAll(trendingWeeklyLink, self.allTrendingWeeklyTitles, pages, "title")
        showAllTrendingData.showAll(trendingTodayLink, self.allTrendingTodayOverviews, pages, "overview")
        showAllTrendingData.showAll(trendingWeeklyLink, self.allTrendingWeeklyOverviews, pages, "overview")
        #showAllTrendingData.showAll(trendingMoviesTodayLink, self.allPopularMovieTitlesTemp, pages, "title")
        showAllTrendingData.showAll(trendingTodayLink, self.allTrendingTodayRatings, pages, "rating")
        showAllTrendingData.showAll(trendingWeeklyLink, self.allTrendingWeeklyRatings, pages, "rating")
        showAllTrendingData.showAll(trendingTodayLink, self.allTrendingTodayGenresID, pages, "genre")
        self.allTrendingTodayGenresName = showAllTrendingData.convertGenreKeys(self.allTrendingTodayGenresID)

        #print(showAllTrendingData.findTrailer("/all", "/571384"))

        # return arrays with info
        return self.allTrendingTodayPosters, self.allTrendingWeeklyPosters, self.allTrendingTodayTitles, self.allTrendingWeeklyTitles,
        self.allTrendingTodayOverviews, self.allTrendingWeeklyOverviews, self.allTrendingTodayRatings, self.allTrendingWeeklyRatings,
        self.allTrendingTodayGenresName


    # run all poster functions for the home page
    def getAllHomePagePosters(self):
        self.trending()
        self.popular()
        self.showAllHomePage()

        return
