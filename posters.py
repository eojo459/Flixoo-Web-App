from home_page_queries import *
from movies_queries import *
from tv_queries import *

class posters:

    def getAllPosters(self):

        homePagePosters = homePageQueryLinks()
        moviePagePosters = moviePageQueries()
        tvPagePosters = tvPageQueries()

        homePagePosters.trending()
        homePagePosters.popular()

        moviePagePosters.upcomingMovies()
        moviePagePosters.nowPlayingMovies()
        moviePagePosters.trendingMovies()
        moviePagePosters.popularMovies()
        moviePagePosters.topRatedMovies()

        tvPagePosters.trendingTV()
        tvPagePosters.popularTV()
        tvPagePosters.topRatedTV()

        return