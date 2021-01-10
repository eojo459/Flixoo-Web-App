######################################################
##  File:           query_tools.py
##  Description:    Functions that extract the required data from the TMDB API
##  Author:         Emmanuel Ojo
##  Date:           December 17 2020
##  Last Updated:   January 7 2021
######################################################

import requests
import json
from api_key import *


class queryFunctionTools:


    ########################################
    # Title: checkContent
    #
    # Description: Checks what kind of content type the search is (movie or tv show) and formats it properly
    #
    # Details:
    #       - Adds a '/' to the beginning of the content type to format it for the URL query
    #       - returns "/movie" or "/tv"
    #
    #########
    def checkContent(self, contentType, contentID):

        # format our input so it works with our link
        if contentType == "movie":
            contentTypeFormatted = "/movie"
        else:
            contentTypeFormatted = "/tv"

        if "/" not in str(contentID):
            contentIDFormatted = "/" + str(contentID)
            return contentIDFormatted, contentTypeFormatted
        else:
            return contentID, contentTypeFormatted
    

    ########################################
    # Title: findTrailer
    #
    # Description: Checks the database for any YouTube trailers available
    #              Checks for any ['type'] == YouTube key values
    #
    # Details:
    #       - Only returns the youtube video id's
    #
    #########
    def findTrailer(self, contentType, contentID):
        
        if str(contentID) == "No ID available":
            return contentID
            
        contentIDFormatted = self.checkContent(contentType, contentID)[0]
        contentTypeFormatted = self.checkContent(contentType, contentID)[1]

        # api requests
        tmdbAPI = keys()

        # check if we are finding movie or tv content
        if contentTypeFormatted == "/movie" or contentTypeFormatted == "/tv":
            finalUrl = tmdbAPI.getAPIUrl() + contentTypeFormatted + contentIDFormatted + "/videos" + tmdbAPI.getAPIKey()
        else:

            # if we don't know the content type, try movie then tv, else just return no trailer found
            try:
                finalUrl = tmdbAPI.getAPIUrl() + "/movie" + contentIDFormatted + "/videos" + tmdbAPI.getAPIKey()
            except:
                finalUrl = tmdbAPI.getAPIUrl() + "/tv" + contentIDFormatted + "/videos" + tmdbAPI.getAPIKey()

        requestGET = requests.get(finalUrl).json()
        checkPath = json.dumps(requestGET)

        # check if the following key exist
        if 'site' in checkPath:
            if "YouTube" in checkPath:

                # get youtube trailer id
                for item in requestGET['results']:
                    if item['type'] is not None:
                        if item['type'] == 'Trailer':
                            if item['key'] is not None:
                                trailer = item['key']
                                youtubeHTTP = "https://www.youtube.com/embed/"
                                return youtubeHTTP + trailer
        
        return "Trailer not available"


    ########################################
    # Title: findWatchProviders
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
    def findWatchProviders(self, contentType, contentID):
        if str(contentID) == "No ID available":
            return contentID
            
        contentIDFormatted = self.checkContent(contentType, contentID)[0]
        contentTypeFormatted = self.checkContent(contentType, contentID)[1]

        # api requests
        tmdbAPI = keys()

        # check if we are finding movie or tv content
        if contentTypeFormatted == "/movie" or contentTypeFormatted == "/tv":
            finalUrl = tmdbAPI.getAPIUrl() + contentTypeFormatted + contentIDFormatted + "/watch/providers" + tmdbAPI.getAPIKey()
        else:
            # if we don't know the content type, try movie then tv, else just return no trailer found
            try:
                finalUrl = tmdbAPI.getAPIUrl() + "/movie" + contentIDFormatted + "/watch/providers" + tmdbAPI.getAPIKey()
            except:
                finalUrl = tmdbAPI.getAPIUrl() + "/tv" + contentIDFormatted + "/watch/providers" + tmdbAPI.getAPIKey()

        requestGET = requests.get(finalUrl).json()
        checkPath = json.dumps(requestGET)

        # check if the following key exist
        netflixCheck = False
        disneyPlusCheck = False

        if 'CA' in checkPath:
            # check ['flatrate']: provider_name == "Disney Plus" or provider_name == "Netflix"
            if "flatrate" in checkPath:
                if requestGET['results']['CA'] is not None:
                    try:
                        if requestGET['results']['CA']['flatrate'] is not None:
                            # check for netflix
                            try:
                                for item in requestGET['results']['CA']['flatrate']:
                                    if item['provider_name'] is not None:
                                        if item['provider_name'] == "Netflix":
                                            netflixCheck = True
                            except:
                                netflixCheck = False

                            # check for disney plus
                            try:
                                for item in requestGET['results']['CA']['flatrate']:
                                    if item['provider_name'] is not None:
                                        if item['provider_name'] == "Disney Plus":
                                            disneyPlusCheck= True
                            except:
                                disneyPlusCheck = False
                    
                            return netflixCheck, disneyPlusCheck
                    except:
                        return netflixCheck, disneyPlusCheck
                else:
                    return netflixCheck, disneyPlusCheck
        else:
            #return "No streaming services available in your region"
            return netflixCheck, disneyPlusCheck


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
    def getID(self, requestGET, index):
        checkPath = json.dumps(requestGET)

        if "id" in checkPath:
            try:
                if requestGET['results'][index]['id'] is not None:
                    return requestGET['results'][index]['id']
            except:
                return "N/A"
                
        else:
            return "N/A"


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
    def getContentType(self, requestGET, index):
        checkPath = json.dumps(requestGET)

        if 'media_type' in checkPath:
            try:
                if requestGET['results'][index]['media_type'] is not None:
                    return requestGET['results'][index]['media_type']
            except:
                return "N/A"
        else:
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
    def getTitle(self, requestGET, index):
        checkPath = json.dumps(requestGET)

        # check if the following keys exist
        if 'original_title' or 'original_name' in checkPath:

            # each title is named under "original_title" or "original_name", pick whichever one exists
            # but first we want to get the ENGLISH titles so try "name" and "title" first
            try: 
                if requestGET['results'][index]['name']:
                    if requestGET['results'][index]['name'] is not None:
                        return requestGET['results'][index]['name']
                    else:
                        return "N/A"
            except:
                try:
                    if requestGET['results'][index]['title']:
                        if requestGET['results'][index]['title'] is not None:
                            return requestGET['results'][index]['title']
                        else:
                            return "N/A"
                except:
                    try:
                        if requestGET['results'][index]['original_title']:
                            if requestGET['results'][index]['original_title'] is not None:
                                return requestGET['results'][index]['original_title']
                            else:
                                return "N/A"
                    except:
                        if requestGET['results'][index]['original_name']:
                            if requestGET['results'][index]['original_name'] is not None:
                                return requestGET['results'][index]['original_name']
                            else:
                                return "N/A"

        else: 
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
    def getOverview(self, requestGET, index):
        checkPath = json.dumps(requestGET)

        # check if the following key exist
        if 'overview' in checkPath:
            try:
                if requestGET['results'][index]['overview'] is not None:
                    if requestGET['results'][index]['overview'] != "":
                        return requestGET['results'][index]['overview']
                    else:
                        return "No description available."
                else:
                    return "No description available."
            except:
                return "No description available."

        # else key doesn't exist, give default description
        else:
            return "No description available."


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
    # get poster
    def getPoster(self, requestGET, index):
        checkPath = json.dumps(requestGET)

        # check if the following key exists
        if 'poster_path' in checkPath:
            try:
                if requestGET['results'][index]['poster_path'] is not None:
                    if requestGET['results'][index]['poster_path'] != "null":
                        posterURL = requestGET['results'][index]['poster_path']
                        imageURL = "https://image.tmdb.org/t/p/w500"
                        finalURL = imageURL + posterURL
                        return finalURL
                    else:
                        return "/static/images/image_not_available.png"
                else:
                    return "/static/images/image_not_available.png"
            except:
                return "/static/images/image_not_available.png"
                

        # else key doesn't exist, show default poster image
        else:
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
    def getReleaseDate(self, requestGET, index):
        checkPath = json.dumps(requestGET)

        # check if the following key exist
        if 'release_date' or 'first_air_date' in checkPath:

            # each release date is named under "release_date" or "first_air_date", pick whichever one exists
            if requestGET['results'][index] is not None:
                try:
                    if requestGET['results'][index]['release_date'] is not None:
                        if requestGET['results'][index]['release_date'] != "":
                            releaseDate = requestGET['results'][index]['release_date']
                            return (releaseDate[0:4])           # only save the 4 digit release date year
                        else:
                            return "N/A"
                    else:
                        return "N/A"
                except:
                    try:
                        if requestGET['results'][index]['first_air_date'] is not None:
                            if requestGET['results'][index]['first_air_date'] != "":
                                releaseDate = requestGET['results'][index]['first_air_date']
                                return (releaseDate[0:4])
                            else:
                                return "N/A"
                        else:
                            return "N/A"
                    except:
                        return "N/A"
                        
            
            # else key doesn't exist, give default 
            else:
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
    def getRating(self, requestGET, index):
        checkPath = json.dumps(requestGET)

        # check if the following key exist
        if 'vote_average' in checkPath:
            try:
                if requestGET['results'][index] is not None:
                    if requestGET['results'][index]['vote_average'] is not None:
                        if requestGET['results'][index]['vote_average'] == 0:
                            return "TBD"
                        else:
                            return requestGET['results'][index]['vote_average']
                    else:
                        return "TBD"
                else:
                    return "TBD"
            except:
                return "TBD"
            
        # else key doesn't exist, give default rating
        else:
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
    def getGenreIDs(self, requestGET, index):
        checkPath = json.dumps(requestGET)

        # check if the following key exist
        if 'genre_ids' in checkPath:
            #print("genres")
            try:
                if requestGET['results'][index]['genre_ids'] is not None:
                    if requestGET['results'][index]['genre_ids'] != " ":
                        return requestGET['results'][index]['genre_ids']
                    else: 
                        return "N/A"
                else:
                    return "N/A"
            except:
                return "N/A"

        # else key doesn't exist, give default genre
        else:
            return "N/A"


    ########################################
    # Title: convertGenreKeys
    #
    # Description: Replaces all the genre ID's with their corresponding genre names
    #
    # Details:
    #       - MOVIE GENRE LIST DATA = https://api.themoviedb.org/3/genre/movie/list?api_key=<<apikey>>&language=en-US
    #       - TV SHOWS GENRE LIST DATA = https://api.themoviedb.org/3/genre/tv/list?api_key=<<apikey>>&language=en-US
    #       - Checks the genreIDArray list values and replaces the id's with the genre names from the genre dictionary values
    #       - returns the genre name
    #
    #########
    def convertGenreKeys(self, genreIDArray):
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
                continue        # skip, move to the next item
            else:
                # replace genre id with the proper genre name
                index = genreIDArray.index(key)
                genreIDArray[index] = value
        
        # format the string so it's like "Comedy, Fantasy, Drama" (with commas)
        totalGenreLen = len(genreIDArray)
        genreNameArray = []
        
        if totalGenreLen >= 3:
            for index in range(0, totalGenreLen - 2):
                genreNameArray.append(str(genreIDArray[index]) + ", ")

            genreNameArray.append(str(genreIDArray[totalGenreLen - 1]))
        elif totalGenreLen == 2:
            genreNameArray.append(str(genreIDArray[0]) + ", ")
            genreNameArray.append(str(genreIDArray[1]))
        elif totalGenreLen == 1:
            genreNameArray.append(str(genreIDArray[0]))
        else:
            genreNameArray.append("N/A")

        return genreNameArray

    ########################################
    # Title: showAll (Main Function)
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
    def showAll(self, linkArray, popularityDict, totalPages):

        # split url into different variables
        httpUrl = linkArray[0]

        # we are dealing with the specific trending api link
        if linkArray[1] == "/trending":
            linkType = "trending"
            popularity = linkArray[1]
            content = linkArray[2]
            window = linkArray[3]
            apiKey = linkArray[4]
        elif linkArray[1] == "/search":
            # search queries
            linkType = "search"
            popularity = linkArray[1]
            searchType = linkArray[2]
            apiKey = linkArray[3]
            queryStr = linkArray[4]
            searchQuery = linkArray[5]
        else:
            # movies & tv shows api link
            linkType = "other"
            content = linkArray[1]
            popularity = linkArray[2]
            apiKey = linkArray[3]

        page = '&page='
        pageNum = 1
        currentPage = page + str(pageNum)
        totalIndex = 0      # keep track of the total values in the whole dictionary

        # use the trending link
        if linkType == "trending":
            finalUrl = httpUrl + popularity + content + window + apiKey + currentPage
        elif linkType == "search":
            finalUrl = httpUrl + popularity + searchType + apiKey + queryStr + searchQuery
        # else use any other link
        else:
            finalUrl = httpUrl + content + popularity + apiKey

        requestGET = requests.get(finalUrl).json()

        # only get the total amount of results per page
        count = 0
        for item in requestGET['results']:
            count += 1

        # get all the posters and titles for the category
        for pageNumber in range(pageNum, totalPages + 1):
            #print("********** PAGE " + str(pageNumber) + " **********")
            for pageIndex in range (0, count):

                # get id
                contentID = self.getID(requestGET, pageIndex)

                # get content type
                contentType = self.getContentType(requestGET, pageIndex)

                if str(contentType) == "movie":
                    contentTypeCapital = "Movie"
                elif str(contentType) == "tv":
                    contentTypeCapital = "Series"
                else:
                    contentTypeCapital = "N/A"

                # get title
                title = self.getTitle(requestGET, pageIndex)
                #print(title)

                # get overview
                overview = self.getOverview(requestGET, pageIndex)

                # get poster
                poster = self.getPoster(requestGET, pageIndex)

                # get get release date
                release = self.getReleaseDate(requestGET, pageIndex)

                # get ratings
                ratings = self.getRating(requestGET, pageIndex)

                # get genres
                tempGenreIDArray = []
                tempGenreIDArray = self.getGenreIDs(requestGET, pageIndex)

                if str(tempGenreIDArray) != "N/A":
                    genres = []
                    genres = self.convertGenreKeys(tempGenreIDArray)
                else:
                    genres = "N/A"
                
                # get trailer
                trailer = self.findTrailer(contentType, contentID)
                
                ## get watch providers
                # generate search term
                searchTermNoSpace = title.replace(" ", "%20")

                # check if netflix exists
                try:
                    if self.findWatchProviders(contentType, contentID)[0] == True:
                        netflixHTTP = "https://www.netflix.com/search?q=" + searchTermNoSpace
                    else:
                        netflixHTTP = "N/A"
                except:
                    netflixHTTP = "N/A"

                # check if disney plus exists
                try:
                    if self.findWatchProviders(contentType, contentID)[1] == True:
                        disneyHTTP = "https://www.disneyplus.com/search"                    # idk how to find disney plus movies lol
                    else:
                        disneyHTTP = "N/A"
                except:
                    disneyHTTP = "N/A"

                if netflixHTTP == "N/A" and disneyHTTP == "N/A":
                    providers = ["N/A", "N/A"]
                else:
                    providers = [netflixHTTP, disneyHTTP]

                ## store all data into dictionary ##
                # [index][0] = contentID
                # [index][1] = contentType
                # [index][2] = title
                # [index][3] = overview
                # [index][4] = poster
                # [index][5] = release
                # [index][6] = rating
                # [index][7][0] = genres
                # [index][8] = trailer
                # [index][9][0] = providers
                popularityDict[totalIndex] = [contentID, contentTypeCapital, title, overview, poster, release, ratings, genres, trailer, providers]
                totalIndex += 1

            # move to next page
            pageNum += 1
            currentPage = page + str(pageNum)

            # update the link with the new page
            if linkType == "trending":
                finalUrl = httpUrl + popularity + content + window + apiKey + currentPage
            elif linkType == "search":
                finalUrl = httpUrl + popularity + searchType + apiKey + queryStr + searchQuery + currentPage
            else:
                finalUrl = httpUrl + content + popularity + apiKey + currentPage

            requestGET = requests.get(finalUrl).json()

            # only get the total amount of results per page
            count = 0
            for item in requestGET['results']:
                count += 1

            # repeat until page = totalPages

        #print("===== ALL DATA LOADED =====")
        return
