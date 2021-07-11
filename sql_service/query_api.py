######################################################
##  File:           query_api.py
##  Description:    Functions that extract the required data from the TMDB API
##  Author:         Emmanuel Ojo
##  Date:           July 11 2021
##  Last Updated:   
######################################################  

from .populate_sql_tables import *
from .mysql_connection import *
from typing import final
import requests
import json

from requests.api import post
from requests.models import requote_uri
from api_key import *
from .query_links import *


class queryResult():

    ########################################
    # Title: queryResultMain
    #
    # Description: Gets all the information for each content type
    #
    # Details:
    #       - Gets the id, content type, title, overview, poster, release date, ratings, genres, trailer, watch providers for 1 content type
    #       - repeats the process 20 times per page for a total of totalPages
    #       - each popularity category uses this (trending today, trending weekly, popular movies, etc)
    #       - returns all the required values to complete the dictionary for one content type
    #
    # TODO:
    #       - add recommendations/similar contents for each content type
    #########

    def queryResultMain(self, updateDB):

        if (updateDB == False):
            print("Update = False, will not update Database")
            return

        # api url/key object
        tmdbAPI = keys()

        # query link object
        queryLink = queryAPILinks()

        # query links + page number
        upcomingMoviesLink = queryLink.getUpcomingMoviesLink()
        nowPlayingMoviesLink = queryLink.getNowPlayingMoviesLink()
        popularMoviesLink = queryLink.getPopularMoviesLink()
        topRatedMoviesLink = queryLink.getTopRatedMoviesLink()
        trendingMoviesTodayLink = queryLink.getTrendingMoviesTodayLink()
        trendingMoviesWeeklyLink = queryLink.getTrendingMoviesWeeklyLink()
        popularTVShowsLink = queryLink.getPopularTVShowsLink()
        topRatedTVShowsLink = queryLink.getTopRatedTVShowsLink()
        trendingTVShowsTodayLink = queryLink.getTrendingTVShowsTodayLink()
        trendingTVShowsWeeklyLink = queryLink.getTrendingTVShowsWeeklyLink()
        trendingAllTodayLink = queryLink.getTrendingAllTodayLink()
        trendingAllWeeklyLink = queryLink.getTrendingAllWeeklyLink()

        # set total pages to go through
        totalPages = 10

        print("--- MOVIES ---")
        print("Getting Popular Movies... ")
        self.getQueryResults(popularMoviesLink, totalPages, "popular-Movies")

        print("Getting Upcoming Movies...")
        self.getQueryResults(upcomingMoviesLink, totalPages, "upcoming-Movies")

        print("Getting Now Playing Movies...")
        self.getQueryResults(nowPlayingMoviesLink, totalPages, "now-Playing-Movies")

        print("Getting Top Rated Movies...")
        self.getQueryResults(topRatedMoviesLink, totalPages, "top-Rated-Movies")

        print("Getting Trending Today Movies...")
        self.getQueryResults(trendingMoviesTodayLink, totalPages, "trending-Today-Movies")

        print("Getting Trending Weekly Movies...")
        self.getQueryResults(trendingMoviesWeeklyLink, totalPages, "trending-Weekly-Movies")

        print("--- TV SHOWS ---")
        print("Getting Popular TV Shows...")
        self.getQueryResults(popularTVShowsLink, totalPages, "popular-TV-Shows")

        print("Getting Top Rated TV Shows...")
        self.getQueryResults(topRatedTVShowsLink, totalPages, "top-Rated-TV-Shows")

        print("Getting Trending Today TV Shows...")
        self.getQueryResults(trendingTVShowsTodayLink, totalPages, "trending-Today-TV-Shows")

        print("Getting Trending Weekly TV Shows...")
        self.getQueryResults(trendingTVShowsWeeklyLink, totalPages, "trending-Weekly-TV-Shows")

        print("--- ALL ---")
        #print("Getting All Popular TV Shows...")
        #self.getQueryResults(popularTVShowsLink, totalPages, "ALL-TV-Shows")

        #print("Getting All Popular Movies...")
        #self.getQueryResults(popularMoviesLink, totalPages, "ALL-Movies")

        print("Getting All Trending Today...")
        self.getQueryResults(trendingAllTodayLink, totalPages, "ALL-Trending-Today")
        
        print("Getting All Trending Weekly...")
        self.getQueryResults(trendingAllWeeklyLink, totalPages, "ALL-Trending-Weekly")

        print("####### All databases updated #######")


    def getQueryResults(self, link, totalPages, sqlTable):

        # starting page number
        pageNum = 1
        originalLink = link
        pageLink = link
        pageLink += str(pageNum)
        #print(pageLink)

        # connect to GET request from api
        requestGET = requests.get(pageLink).json()

        # get json path
        path = json.dumps(requestGET)

        # count the results
        resultCount = 0

        for item in requestGET['results']:
            resultCount += 1

        # keep track of popularity/rankings
        ranking = 1

        # list of records to be inserted into sql databases
        records = []

        # get all the results on the current page for all totalPages
        for pageNumber in range(1, totalPages + 1):
            #print("PAGE # " + str(pageNumber))

            # get all the api data for each result on the current page (20 results per page 0->19)
            for pageIndex in range(0, resultCount):

                ## get id
                contentID = self.getID(requestGET, path, pageIndex)
                #print(str(pageIndex) + " " + str(contentID))

                ## get content type
                contentType = self.getContentType(requestGET, path, pageIndex)

                if str(contentType) == "movie":
                    contentType = "Movie"
                elif str(contentType) == "tv":
                    contentType = "Series"
                else:
                    contentType = "N/A"

                ## get title
                title = self.getTitle(requestGET, path, pageIndex)

                ## get overview
                overview = self.getOverview(requestGET, path, pageIndex)

                ## get poster
                poster = self.getPoster(requestGET, path, pageIndex)

                ## get release date
                releaseDate = self.getReleaseDate(requestGET, path, pageIndex)

                ## get ratings
                rating = self.getRating(requestGET, path, pageIndex)

                ## get genres
                genres = self.getGenre(requestGET, path, pageIndex)

                ## get trailer (youtube)
                trailer = self.getTrailer(contentType, contentID)
            
                ## get watch providers (netflix, disney plus, etc..)
                watchProviders = self.getWatchProviders(contentType, contentID)

                
                # generate search term
                searchTermNoSpace = title.replace(" ", "%20")

                # check if netflix exists
                try:
                    if watchProviders[0] == True:
                        netflixHTTP = "https://www.netflix.com/search?q=" + searchTermNoSpace
                    else:
                        netflixHTTP = "N/A"
                except:
                    netflixHTTP = "N/A"

                # check if disney plus exists
                try:
                    if watchProviders[1] == True:
                        disneyHTTP = "https://www.disneyplus.com/search"   # idk how to find disney plus movies lol
                    else:
                        disneyHTTP = "N/A"
                except:
                    disneyHTTP = "N/A"

                if netflixHTTP == "N/A" and disneyHTTP == "N/A":
                    providers = "N/A"
                elif netflixHTTP =="N/A" and disneyHTTP != "N/A":
                    providers = disneyHTTP
                elif netflixHTTP !="N/A" and disneyHTTP == "N/A":
                    providers = netflixHTTP
                else:
                    providers = "N/A"
                

                #print("ID: " + str(contentID))
                #print("Type: " + contentType)
                #print("Title: " + title)
                #print("Rank #" + str(ranking) + " | Type: " + contentType + " | Title: " + title)
                #print("Overview: " + overview)
                #print("Poster: " + poster)
                #print("Release: " + str(releaseDate))
                #print("Rating: " + str(rating))
                #print("Genres: " + str(genres))
                #print("Trailer: " + str(trailer))
                #print("Providers: " + str(providers))

                # add results to a record list, this list will be inserted into sql table
                records.append((contentID, ranking, contentType, title, overview, poster, releaseDate, rating, genres, trailer, str(providers)))
                ranking += 1
               

            # update page number, move to next page
            pageNum += 1
            pageLink = originalLink
            pageLink += str(pageNum)
            #print(pageLink)

            # connect to GET request from api
            requestGET = requests.get(pageLink).json()

            # get json path
            path = json.dumps(requestGET)

            # count the results
            resultCount = 0

            for item in requestGET['results']:
                resultCount += 1

        #print(records[0][0])
        #print(records[0])

        # sql table queries object
        sqlDB = populateTables()

        # insert/update data in database from records
        sqlDB.updateSQLTable(records, sqlTable)


    ########################################
    # Title: getContentType
    #
    # Description: Checks the database for the content type of the specific content
    #
    # Details:
    #       - Checks for any ['media_type'] keys and returns the corresponding value of the key
    #       - returns "movie" or "tv", else return "N/A"
    #
    #########

    def getContentType(self, requestGET, path, index):
        
        try:
            if 'media_type' in path:
                try:
                    contentTypePath = requestGET['results'][index]['media_type']
                    if contentTypePath is not None:
                        return contentTypePath
                except:
                    return "N/A"
            return "N/A"
        except:
            return "N/A"


    ########################################
    # Title: getID
    #
    # Description: Checks the database for the ID of the specific content
    #
    # Details:
    #       - Checks for any ['id'] keys and returns the corresponding value of the key
    #       - returns the id of the content, else returns "N/A"
    #
    #########

    def getID(self, requestGET, path, index):

        #idPath = requestGET['results'][index]['id']

        try:
            if 'id' in path:
                try:
                    idPath = requestGET['results'][index]['id']
                    if idPath is not None:
                        return idPath
                except:
                    return "N/A"
                return "N/A"
            else:
                return "N/A"
        except:
            return "N/A"


    ########################################
    # Title: getTitle
    #
    # Description: Checks the database for the content title name of the specific content
    #
    # Details:
    #       - Checks for any ['original_title'] or ['original_name'] keys and returns the corresponding value of the key
    #       - returns the title name of the movie/tv show, else return "N/A"
    #
    #########

    def getTitle(self, requestGET, path, index):

        #namePath = requestGET['results'][index]['name']
        #titlePath = requestGET['results'][index]['title']
        #originalTitlePath = requestGET['results'][index]['original_title']
        #originalNamePath = requestGET['results'][index]['original_name']

        # check if these keys exist first..
        try:
            if 'original_title' or 'original_name' in path:

                # each title is named under "name", "title", "original_title" or "original_name", pick whichever one exists
                # but first we want to get the ENGLISH titles so try "name" and "title" first
                try:
                    namePath = requestGET['results'][index]['name']
                    if namePath is not None:
                        return namePath
                except:
                    try: 
                        titlePath = requestGET['results'][index]['title']
                        if titlePath is not None:
                            return titlePath
                    except:
                        try:
                            originalTitlePath = requestGET['results'][index]['original_title']
                            if originalTitlePath is not None:
                                return originalTitlePath
                        except:
                            try:
                                originalNamePath = requestGET['results'][index]['original_name']
                                if originalNamePath is not None:
                                    return originalNamePath
                            except:
                                return "N/A"
                return "N/A"
            else:
                return "N/A"
        except:
            return "N/A"
        

    ########################################
    # Title: getOverview
    #
    # Description: Checks the database for the description/overview of the specific content
    #
    # Details:
    #       - Checks for any ['overview'] keys and returns the corresponding value of the key
    #       - returns the movie/tv show description, else return "No description available"
    #
    #########

    def getOverview(self, requestGET, path, index):
        
        try:
            if 'overview' in path:
                try:
                    overviewPath = requestGET['results'][index]['overview']
                    if overviewPath is not None:
                        if overviewPath != "":
                            return overviewPath
                except:
                    return "N/A"
                return "N/A"
            else:
                return "N/A"
        except:
            return "N/A"

    
    ########################################
    # Title: getPoster
    #
    # Description: Checks the database for the poster image path of the specific content
    #
    # Details:
    #       - Checks for any ['poster_path'] keys and returns the corresponding value of the key
    #       - returns the link to the poster image else, return a default no image available picture
    #
    #########

    def getPoster(self, requestGET, path, index):

        try:
            if 'poster_path' in path:
                posterPath = requestGET['results'][index]['poster_path'] 
                if posterPath is not None:
                    if posterPath != "null":
                        imageURL = "https://image.tmdb.org/t/p/w500"
                        finalURL = imageURL + posterPath
                        return finalURL
            return "/static/images/image_not_available.png"
        except:
            return "/static/images/image_not_available.png"


    ########################################
    # Title: getReleaseDate
    #
    # Description: Checks the database for the release date of the specific content
    #
    # Details:
    #       - Checks for any ['release_date'] or ['first_air_date'] keys and returns the corresponding value of the key
    #       - returns the release date (year only), else return "N/A"
    #
    #########

    def getReleaseDate(self, requestGET, path, index):

        try:
            if 'release_date' or 'first_air_date' in path:

                # each release date is named under "release_date" or "first_air_date", pick whichever one exists
                try:
                    releaseDatePath = requestGET['results'][index]['release_date']
                    if releaseDatePath is not None:
                        if releaseDatePath != "":
                            return releaseDatePath[0:4]
                    return "N/A"
                except:
                    try:
                        firstAirDatePath = requestGET['results'][index]['first_air_date']
                        if firstAirDatePath is not None:
                            if firstAirDatePath != "":
                                return firstAirDatePath[0:4]
                        return "N/A"
                    except:
                        return "N/A"
            return "N/A"
        except:
            return "N/A"


    ########################################
    # Title: getRating
    #
    # Description: Checks the database for the rating of the specific content
    #
    # Details:
    #       - Checks for any ['vote_average'] keys and returns the corresponding value of the key
    #       - returns the rating, else return "TBD"
    #
    #########

    def getRating(self, requestGET, path, index):

        try: 
            if 'vote_average' in path:
                try:
                    ratingPath = requestGET['results'][index]['vote_average']
                    if ratingPath is not None:
                        if ratingPath == 0:
                            return "TBD"
                        else:
                            return ratingPath
                except:
                    return "TBD"
            return "TBD"
        except:
            return "TBD"


    ########################################
    # Title: getGenreIDs
    #
    # Description: Checks the database for the genre id's of the specific content
    #
    # Details:
    #       - Checks for any ['genre_ids'] keys and returns the corresponding value of the keys
    #       - returns all the genre id's, else return "N/A"
    #
    #########

    def getGenreID(self, requestGET, path, index):
        try:
            if 'genre_ids' in path:
                try:
                    genreIDPath = requestGET['results'][index]['genre_ids']
                    if genreIDPath is not None:
                        if genreIDPath != " ":
                            return genreIDPath
                except:
                    return "N/A"
            return "N/A"
        except:
            return "N/A"
            

    ########################################
    # Title: getGenre
    #
    # Description: Replaces all the genre ID's with their corresponding genre names
    #
    # Details:
    #       - MOVIE GENRE LIST DATA = https://api.themoviedb.org/3/genre/movie/list?api_key=<<apikey>>&language=en-US
    #       - TV SHOWS GENRE LIST DATA = https://api.themoviedb.org/3/genre/tv/list?api_key=<<apikey>>&language=en-US
    #       - Calls getGenreID and converts the ID into the genre name
    #       - returns the genre name
    #
    #########
    
    def getGenre(self, requestGET, path, index):

        # get the ID's for the genres
        genreIDArray = self.getGenreID(requestGET, path, index)

        # local genres dictionary
        genres = {
            28: "Action",
            53: "Thriller",
            80: "Crime",
            12: "Adventure",
            16: "Animation",
            35: "Comedy",
            18: "Drama",
            10751: "Family",
            14: "Fantasy",
            99: "Documentary",
            36: "History",
            27: "Horror",
            10402: "Music",
            9648: "Mystery",
            10749: "Romance",
            878: "Science-Fiction",
            10770: "TV Movie",
            10752: "War",
            37: "Western",
            10759: "Action & Adventure",
            10762: "Kids",
            10763: "News",
            10764: "Reality",
            10765: "Sci-Fi & Fantasy",
            10766: "Soap",
            10767: "Talk",
            10768: "War & Politics",
        }

        # replace all id's with their correct names from the genre dictionary
        for key, value in genres.items():
            if key not in genreIDArray:
                continue        # skip, move to next item in the array
            else:
                # replace ID with the proper genre name
                index = genreIDArray.index(key)
                genreIDArray[index] = value

        # format the string so it's like "Comedy, Fantasy, Drama" (with commas after each value)
        totalGenreLen = len(genreIDArray)
        #genreNameArray = []
        genreNameText = ""

        if totalGenreLen >= 3:
            # add commas after every item in the array if it's not the last value
            for index in range(0, totalGenreLen - 2):
                #genreNameArray.append(str(genreIDArray[index]) + ", ")
                genreNameText += str(genreIDArray[index]) + ", "
            
            #genreNameArray.append(str(genreIDArray[totalGenreLen - 1])) # last value, dont add a comma
            genreNameText += str(genreIDArray[totalGenreLen - 1])

        elif totalGenreLen == 2:
            #genreNameArray.append(str(genreIDArray[0]) + ", ") # add comma after first value
            #genreNameArray.append(str(genreIDArray[1])) # last value, dont add a comma
            genreNameText += str(genreIDArray[0]) + ", "
            genreNameText += str(genreIDArray[1])

        elif totalGenreLen == 1:
            #genreNameArray.append(str(genreIDArray[0])) # one value, dont add a comma
            genreNameText += str(genreIDArray[0])

        else:
            #genreNameArray.append("N/A")
            genreNameText += "N/A"

        #return genreNameArray
        return genreNameText

    ########################################
    # Title: getTrailer
    #
    # Description: Checks the database for any YouTube trailers available
    #              Checks for any ['type'] == YouTube key values
    #
    # Details:
    #       - Only returns the youtube video id's
    #
    #########

    def getTrailer(self, contentType, contentID):

        # api url/key object
        tmdbAPI = keys()
        
        # convert content type to lower case/reformat for link
        if contentType == "Movie":
            contentType = "movie"

        elif contentType == "Series":
            contentType = "tv"

        # format ID -> ex. "/1234" | format content -> ex. "/movie" or "/tv"
        contentIDFormatted = "/" + str(contentID)
        contentTypeFormatted = "/" + contentType
        finalURL = ""

        # get videos/trailer api url
        if contentTypeFormatted == "/movie" or contentTypeFormatted == "/tv":
            finalURL = "https://api.themoviedb.org/3" + contentTypeFormatted + str(contentIDFormatted) + "/videos" + tmdbAPI.getAPIKey() + "&language=en-US"
        else:
            return "Trailer not available"

        requestGET = requests.get(finalURL).json()
        path = json.dumps(requestGET)
        
        try:
            # check if the following key exist
            if 'site' in path:
                if "YouTube" in path:

                    # get youtube trailer id
                    for item in requestGET['results']:
                        if item['type'] is not None:
                            if item['type'] == 'Trailer':
                                if item['key'] is not None:
                                    trailer = item['key']
                                    youtubeHTTP = "https://www.youtube.com/embed/"
                                    return youtubeHTTP + trailer
        except:
            return "Trailer not available"
        
        return "Trailer not available"
        
    
    ########################################
    # Title: getWatchProviders
    #
    # Description: Checks the database for any streaming watch providers available
    #              Checks for any ['flatrate'] key values
    #
    # Details:
    #       - Only supports CANADA region
    #       - Supports Netflix (CANADA) (Searches the movie/tv show title name for the user)
    #       - Partially supports Disney plus (brings user to search page for them to search themself)
    #       - returns true or false depending on it's availability on Netflix or Disney plus in the region
    #
    # TODO:
    #       - Planning to add more supported watch providers (hulu, amazon prime, etc)
    #       - Support more regions (USA, UK, etc)
    #       - Maybe auto start the movie/tv show for the user if possible?
    #########

    def getWatchProviders(self, contentType, contentID):

        # api url/key object
        tmdbAPI = keys()
        
        # convert content type to lower case/reformat for link
        if contentType == "Movie":
            contentType = "movie"

        elif contentType == "Series":
            contentType = "tv"

        # format ID -> ex. "/1234" | format content -> ex. "/movie" or "/tv"
        contentIDFormatted = "/" + str(contentID)
        contentTypeFormatted = "/" + contentType
        finalURL = ""

        # get watch providers api url
        if contentTypeFormatted == "/movie" or contentTypeFormatted == "/tv":
            finalURL = "https://api.themoviedb.org/3" + contentTypeFormatted + str(contentIDFormatted) + "/watch/providers" + tmdbAPI.getAPIKey() + "&language=en-US"
        else:
            return "No providers in your region"

        requestGET = requests.get(finalURL).json()
        path = json.dumps(requestGET)

        # check if the following key exist
        netflixCheck = False
        disneyPlusCheck = False

        # check for netflix
        try:
            if 'CA' in path:
                if 'flatrate' in path:
                    canadaPath = requestGET['results']['CA']
                    if canadaPath is not None:
                        flatRatePath = requestGET['results']['CA']['flatrate']
                        if flatRatePath is not None:
                            for item in flatRatePath:
                                if item['provider_name'] is not None:
                                    if item['provider_name'] == "Netflix":
                                        netflixCheck = True
        except:
            netflixCheck = False
        
        # check for disney plus
        try:
            if 'CA' in path:
                if 'flatrate' in path:
                    canadaPath = requestGET['results']['CA']
                    if canadaPath is not None:
                        flatRatePath = requestGET['results']['CA']['flatrate']
                        if flatRatePath is not None:
                            for item in flatRatePath:
                                if item['provider_name'] is not None:
                                    if item['provider_name'] == "Disney Plus":
                                        disneyPlusCheck = True
        except:
            disneyPlusCheck = False

        return netflixCheck, disneyPlusCheck








