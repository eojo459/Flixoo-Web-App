import requests
import json
from api_key import *

# MOVIE GENRE LIST: https://api.themoviedb.org/3/genre/movie/list?api_key=<<apikey>>&language=en-US
# TV SHOWS GENRE LIST: https://api.themoviedb.org/3/genre/tv/list?api_key=<<apikey>>&language=en-US


class queryFunctionTools:

    # loop through the json data and find the ['poster_path] values
    # append the imageURL with poster link to get full image poster link, add to array
    def findPosterPath(self, requestJson, posterArray):
        
        checkPath = json.dumps(requestJson)

        # check if the following key exists
        if 'poster_path' in checkPath:
            for item in requestJson['results']:
                if item['poster_path'] is not None:
                    posterURL = item['poster_path']
                    imageURL = "https://image.tmdb.org/t/p/w500"
                    finalURL = imageURL + posterURL
                    posterArray.append(finalURL)

        # else key doesn't exist, show default poster image
        else:
            posterArray.append("/static/images/image_not_available.png")
                
        return


    # get the titles
    def findTitlePath(self, requestJson, titleArray):

        checkPath = json.dumps(requestJson)

        # check if the following keys exist
        if 'original_title' or 'original_name' in checkPath:

            # each title is named under "original_title" or "original_name", pick whichever one exists
            for item in requestJson['results']:
                try:
                    if item['original_title'] is not None:
                        titleName = item['original_title']
                        titleArray.append(titleName)
                    else:
                        titleArray.append("N/A")
                except:
                    if item['original_name'] is not None:
                        titleName = item['original_name']
                        titleArray.append(titleName)
                    else:
                        titleArray.append("N/A")

        # else keys don't exist, give default title
        else:
            titleArray.append("N/A")

        return


    # get overview descriptions
    def findOverviewPath(self, requestJson, overviewArray):

        checkPath = json.dumps(requestJson)

        # check if the following key exist
        if 'overview' in checkPath:

            for item in requestJson['results']:
                if item['overview'] is not None:
                    overviewDescription = item['overview']
                    overviewArray.append(overviewDescription)

        # else key doesn't exist, give default description
        else: 
            overviewArray.append("No description available.")

        return

    # get ratings
    def findRatingPath(self, requestJson, ratingArray):

        checkPath = json.dumps(requestJson)

        # check if the following key exist
        if 'vote_average' in checkPath:

            for item in requestJson['results']:
                if item['vote_average'] is not None:
                    rating = item['vote_average']
                    ratingArray.append(rating)

        # else key doesn't exist, give default rating
        else:
            ratingArray.append("TBD")

        return

    
    # get genres
    def findGenrePath(self, requestJson, genreArrayID):

        checkPath = json.dumps(requestJson)

        # check if the following key exist
        if 'genre_ids' in checkPath:
            #print("genres")

            for item in requestJson['results']:
                if item['genre_ids'] is not None:
                    genre = item['genre_ids']
                    genreArrayID.append(genre)

        # else key doesn't exist, give default genre
        else:
            genreArray.append("Unknown")

        return

    # convert the genre ids to actual genre names
    def convertGenreKeys(self, genreIDArray):

        genreNameArray = []
        
        # genres dictionary
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
            10770: "TV-Movie",
            10752: "War",
            37: "Western",
            10759: "Action-&-Adventure",
            10762: "Kids",
            10763: "News",
            10764: "Reality",
            10765: "Sci-Fi-&-Fantasy",
            10766: "Soap",
            10767: "Talk",
            10768: "War-&-Politics",
        }

        # replace all id's with their correct names from the genre dictionary
        for id in genreIDArray:
            genreNameArray.append([genres.get(x, x) for x in id])

        #genreIDArray = genreNameArray
        #print(genreNameArray)
        return genreNameArray

    # get content ID numbers
    def findContentID(self, requestJson, contentIDArray):
        
        checkPath = json.dumps(requestJson)

        # check if the following key exist
        if 'id' in checkPath:

            for item in requestJson['results']:
                if item['id'] is not None:
                    contentID = item['id']
                    contentIDArray.append(contentID)

        # else key doesn't exist, give default message
        else: 
            contentIDArray.append("No ID available")

        return

    def findTrailer(self, contentType, contentID):

        # format our input so it works with our link
        if contentType == "movie":
            contentTypeFormatted = "/movie"
        else:
            contentTypeFormatted = "/tv"

        if "/" not in str(contentID):
            contentIDFormatted = "/" + str(contentID)

        # api requests
        tmdbLink = keys()
        apiKey = keys()

        # check if we are finding movie or tv content
        if contentTypeFormatted == "/movie" or contentTypeFormatted == "/tv":
            finalUrl = tmdbLink.getAPIUrl() + contentTypeFormatted + contentIDFormatted + "/videos" + apiKey.getAPIKey()
        else:

            # if we don't know the content type, try movie then tv, else just return no trailer found
            try:
                finalUrl = tmdbLink.getAPIUrl() + "/movie" + contentIDFormatted + "/videos" + apiKey.getAPIKey()
            except:
                finalUrl = tmdbLink.getAPIUrl() + "/tv" + contentIDFormatted + "/videos" + apiKey.getAPIKey()
                
        requestJson = requests.get(finalUrl).json()
        
        checkPath = json.dumps(requestJson)

        # check if the following key exist
        if 'site' in checkPath:
            if "YouTube" in checkPath:

                # get youtube trailer id
                for item in requestJson['results']:
                    if item['type'] is not None:
                        if item['type'] == 'Trailer':
                            if item['key'] is not None:
                                trailer = item['key']
                                return trailer

        return "Trailer not available"
        
    # use a search term to find an ID
    def singleSearch(self, searchTerm):
        
        # api requests
        tmdbLink = keys()
        apiKey = keys()
    
        # setup the api GET link
        searchTermNoSpace = searchTerm.replace(" ", "%20")
        finalUrl = tmdbLink.getAPIUrl() + "/search/multi" + apiKey.getAPIKey() + "&query=" + searchTermNoSpace
        requestJson = requests.get(finalUrl).json()
        
        checkPath = json.dumps(requestJson)

        # check if the following keys exist
        if 'original_title' or 'original_name' in checkPath:

            # each title is named under "original_title" or "original_name", pick whichever one exists
            for item in requestJson['results']:
                
                # find title name then return id
                try:
                    if item['original_title'] is not None:
                        if searchTerm == item['original_title']:
                            contentID = item['id']
                            contentType = item['media_type']
                            break
                    else:
                        return "No ID"
                except:
                    if item['original_name'] is not None:
                        if searchTerm == item['original_name']:
                            contentID = item['id']
                            contentType = item['media_type']
                            break
                    else:
                        return "No ID"

        # else keys don't exist, give default
        else:
            return "No ID"
        
        return self.findTrailer(contentType, contentID)
        
    def findReleaseDate(self):
        pass


    # SHOW ALL THE SELECTED INFORMATION FOR A CATEGORY
    def showAll(self, linkArray, typeArray, totalPages, toolType):

        # split url into different variables
        httpUrl = linkArray[0]

        # we are dealing with the specific trending api link
        if linkArray[1] == "/trending":
            linkType = "trending"
            popularity = linkArray[1]
            content = linkArray[2]
            window = linkArray[3]
            apiKey = linkArray[4]

        else:
            # movies & tv shows api link
            linkType = "other"
            content = linkArray[1]
            popularity = linkArray[2]
            apiKey = linkArray[3] 
        
        page = '&page='
        pageNum = 1
        currentPage = page + str(pageNum)

        # use the trending link
        if linkType == "trending":
            finalUrl = httpUrl + popularity + content + window + apiKey + currentPage

        # else use any other link
        else:
            finalUrl = httpUrl + content + popularity + apiKey

        requestJson = requests.get(finalUrl).json()

        # get all the posters for the category
        for pageNumber in range(pageNum,totalPages):

            # get content id
            if toolType == "id":
                self.findContentID(requestJson, typeArray)
            # get posters
            elif toolType == "poster":
                self.findPosterPath(requestJson, typeArray)
            # get titles
            elif toolType == "title":
                self.findTitlePath(requestJson, typeArray)
            # get overview descriptions
            elif toolType == "overview":
                self.findOverviewPath(requestJson, typeArray)
            # get ratings
            elif toolType == "rating":
                self.findRatingPath(requestJson, typeArray)
            # get genres
            elif toolType == "genre":
                self.findGenrePath(requestJson, typeArray)

            # move to next page
            pageNum += 1
            currentPage = page + str(pageNum)

            # update the link with the new page
            if linkType == "trending":
                finalUrl = httpUrl + popularity + content + window + apiKey + currentPage
            else:
                finalUrl = httpUrl + content + popularity + apiKey + currentPage

            requestJson = requests.get(finalUrl).json()
            #print(finalUrl)

            # print next 20 titles
            # repeat until page = totalPages (100+ films total)