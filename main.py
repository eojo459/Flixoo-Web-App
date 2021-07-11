######################################################
##  File:           main.py
##  Description:    Main file for the Flixoo Flask Website Application
##  Author:         Emmanuel Ojo
##  Date:           December 17 2020
##  Last Updated:   July 10 2021
######################################################   

import time
from flask import Flask, render_template, request
from api_key import *
from home_page_queries import *
from movies_queries import *
from search_queries import *
from apscheduler.schedulers.background import BackgroundScheduler

## July 10 2021 UPDATE: Updated code so that it now functions properly with the sql database (search still uses old query method)

app = Flask(__name__)

### LOAD OBJECTS WITH DATA FOR THE WEBSITE ###
print("--- App is starting ---")
homeQuery = homePageQueryLinks()
homeQuery.showAllHomePage()
movieQuery = moviePageQueries()
movieQuery.showAllMoviePage()
tvQuery = tvPageQueries()
tvQuery.showAllTVPage()
searchQuery = searchQueryLinks()
print("--- All data has been loaded! ---")


# function to query the db and get fresh results
def queryDB():
    print("Querying database tables...")
    homeQuery.showAllHomePage()
    movieQuery.showAllMoviePage()
    tvQuery.showAllTVPage()
    print("Results have been updated!")


# scheduler to query database every 60 minutes (1 hour)
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(queryDB, 'interval', minutes=60)
scheduler.start()


### HOME PAGE ###
@app.route("/", methods = ['GET'])
@app.route("/home", methods = ['GET'])
def home():
    print("home page loading")
    time.sleep(1.5)
    return render_template("home.html", homeQuery=homeQuery, movieQuery=movieQuery, tvQuery=tvQuery)
    #return render_template("home.html", homeQuery=homeQuery, tvQuery=tvQuery)

@app.route("/all-trending-today")
def showAllTrendingToday():
    time.sleep(1.5)
    return render_template("all-trending-today.html", homeQuery=homeQuery)

@app.route("/all-trending-weekly")
def showAllTrendingWeekly():
    time.sleep(1.5)
    return render_template("all-trending-weekly.html", homeQuery=homeQuery)


### MOVIES ###
@app.route("/movies", methods = ['GET'])
def movies():
    print("movies page loading")
    time.sleep(1.5)
    return render_template("movies.html", movieQuery=movieQuery)

@app.route("/all-upcoming-movies")
def showAllUpcomingMovies():
    time.sleep(1.5)
    return render_template("all-upcoming-movies.html", movieQuery=movieQuery)

@app.route("/all-now-playing-movies")
def showAllNowPlayingMovies():
    time.sleep(1.5)
    return render_template("all-now-playing-movies.html", movieQuery=movieQuery)

@app.route("/all-trending-movies-today")
def showAllTrendingMoviesToday():
    time.sleep(1.5)
    return render_template("all-trending-movies-today.html", movieQuery=movieQuery)

@app.route("/all-trending-movies-weekly")
def showAllTrendingMoviesWeekly():
    time.sleep(1.5)
    return render_template("all-trending-movies-weekly.html", movieQuery=movieQuery)

@app.route("/all-popular-movies")
def showAllPopularMovies():
    time.sleep(1.5)
    return render_template("all-popular-movies.html", movieQuery=movieQuery)

@app.route("/all-top-rated-movies")
def showAllTopRatedMovies():
    time.sleep(1.5)
    return render_template("all-top-rated-movies.html", movieQuery=movieQuery)


### TV SHOWS ###
@app.route("/tvshows")
def tvShows():
    time.sleep(1.5)
    return render_template("tvShows.html", tvQuery=tvQuery)

@app.route("/all-trending-today-tv-shows")
def showAllTrendingTVToday():
    time.sleep(1.5)
    return render_template("all-trending-tv-shows-today.html", tvQuery=tvQuery)

@app.route("/all-trending-weekly-tv-shows")
def showAllTrendingTVWeekly():
    time.sleep(1.5)
    return render_template("all-trending-tv-shows-weekly.html", tvQuery=tvQuery)

@app.route("/all-popular-tv-shows")
def showAllPopularTV():
    time.sleep(1.5)
    return render_template("all-popular-tv-shows.html", tvQuery=tvQuery)

@app.route("/all-top-rated-tv-shows")
def showAllTopRatedTV():
    time.sleep(1.5)
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
    

if __name__ == "__main__":
    print("App is running")
    app.run(host='0.0.0.0')
    #app.run(host='127.0.0.1')
