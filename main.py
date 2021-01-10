######################################################
##  File:           main.py
##  Description:    Main file for the Flixoo Flask Website Application
##  Author:         Emmanuel Ojo
##  Date:           December 17 2020
##  Last Updated:   January 10 2021
######################################################   

from flask import Flask, render_template, request
import requests
from api_key import *
from home_page_queries import *
from movies_queries import *
from search_queries import *
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

### GET DATA FOR THE WEBSITE ###
# Takes ~ 5 minutes - 10 minutes

homeQuery = homePageQueryLinks()
homeQuery.showAllHomePage()
movieQuery = moviePageQueries()
movieQuery.showAllMoviePage()
tvQuery = tvPageQueries()
tvQuery.showAllTVPage()
searchQuery = searchQueryLinks()

"""
print("################################################################")
print("## ALL DATA HAS BEEN LOADED - REFRESH COMPLETE ##")
print("################################################################")
"""

def loadData():
    print("** RETRIEVING NEW DATA **")
    homeQuery = homePageQueryLinks()
    movieQuery = moviePageQueries()
    tvQuery = tvPageQueries()
    homeQuery.showAllHomePage()
    movieQuery.showAllMoviePage()
    tvQuery.showAllTVPage()

# create the scheduler to get new data every 3 hours / 180 minutes in the background
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(loadData, 'interval', minutes=180)
scheduler.start()

### HOME PAGE ###
@app.route("/", methods = ['GET'])
@app.route("/home", methods = ['GET'])
def home():
    print("home page loading")
    return render_template("home.html", homeQuery=homeQuery, movieQuery=movieQuery, tvQuery=tvQuery)
    #return render_template("home.html", homeQuery=homeQuery, tvQuery=tvQuery)

@app.route("/all-trending-today")
def showAllTrendingToday():
    return render_template("all-trending-today.html", homeQuery=homeQuery)

@app.route("/all-trending-weekly")
def showAllTrendingWeekly():
    return render_template("all-trending-weekly.html", homeQuery=homeQuery)

### MOVIES ###
@app.route("/movies", methods = ['GET'])
def movies():
    print("movies page loading")
    return render_template("movies.html", movieQuery=movieQuery)

@app.route("/all-upcoming-movies")
def showAllUpcomingMovies():
    return render_template("all-upcoming-movies.html", movieQuery=movieQuery)

@app.route("/all-now-playing-movies")
def showAllNowPlayingMovies():
    return render_template("all-now-playing-movies.html", movieQuery=movieQuery)

@app.route("/all-trending-movies-today")
def showAllTrendingMoviesToday():
    return render_template("all-trending-movies-today.html", movieQuery=movieQuery)

@app.route("/all-trending-movies-weekly")
def showAllTrendingMoviesWeekly():
    return render_template("all-trending-movies-weekly.html", movieQuery=movieQuery)

@app.route("/all-popular-movies")
def showAllPopularMovies():
    return render_template("all-popular-movies.html", movieQuery=movieQuery)

@app.route("/all-top-rated-movies")
def showAllTopRatedMovies():
    return render_template("all-top-rated-movies.html", movieQuery=movieQuery)

### TV SHOWS ###
@app.route("/tvshows", methods = ['GET'])
def tvShows():
    return render_template("tvShows.html", tvQuery=tvQuery)

@app.route("/all-trending-today-tv-shows")
def showAllTrendingTVToday():
    return render_template("all-trending-tv-shows-today.html", tvQuery=tvQuery)

@app.route("/all-trending-weekly-tv-shows")
def showAllTrendingTVWeekly():
    return render_template("all-trending-tv-shows-weekly.html", tvQuery=tvQuery)

@app.route("/all-popular-tv-shows")
def showAllPopularTV():
    return render_template("all-popular-tv-shows.html", tvQuery=tvQuery)

@app.route("/all-top-rated-tv-shows")
def showAllTopRatedTV():
    return render_template("all-top-rated-tv-shows.html", tvQuery=tvQuery)

## SEARCH BAR ##
@app.route("/search", methods = ['GET','POST'])
def searchData():
    if request.method == "POST":
        searchResults = request.form.get("searchSubmit")
        searchQuery.showAllSearchResults(searchResults)
    else:
        searchResults = ""
        searchQuery.showAllSearchResults(searchResults)
    return render_template("search-results.html", searchQuery=searchQuery, searchResults=searchResults)
    

"""
if __name__ == "__main__":
    print("App is running")
    #scheduler.add_job(id = 'Reload API Data', func=loadData, trigger="interval", seconds=10)
    #scheduler.start()
    app.run(debug=True, threaded=True)
"""


if __name__ == "__main__":
    print("App is running")
    app.run(host='0.0.0.0')
    #app.run(host='127.0.0.1')
