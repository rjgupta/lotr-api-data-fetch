# URL: https://the-one-api.dev/v2
import requests
import json
import csv
import ast
import base64

movieurl = 'https://the-one-api.dev/v2/movie'
# headers = {'Authorization' : 'RBMm0r3qeJaXl6IJBNEz'}
access_token = 'RBMm0r3qeJaXl6IJBNEz'
headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}
movieResponse = requests.get(movieurl, headers=headers)

movieDict = movieResponse.json()
# print(response)
# print(type(movieDict))

# -----------------------------------------------------
# Movies
# movieFile = open('movies.json')
# moviesDict = json.load(movieFile)

movies = movieDict.get("docs")
# print(movies)
tempList = []

for mov in movies:
    for val in mov.values():
        # print(val)
        tempList.append(val)

# IDS:
idList = tempList[0::4]
idListFinal = idList[0::2]
# print(idListFinal)

# Movies
movieList = tempList[1::4]
movieListFinal = movieList[0::2]
# print(movieListFinal)

# making a key value pair for step 4 of the task 

movieIDPair = zip(idListFinal, movieListFinal)
# use it for step 4 
movieIDDict = dict(movieIDPair)
# print(movieIDDict)

# ------------------------------------------------------------
# CHARACTERS: 

characterurl = "https://the-one-api.dev/v2/character"
characterResponse = requests.get(characterurl, headers=headers)

# Characters 
charResponseDict = characterResponse.json()
characters = charResponseDict.get("docs")
characterList = []
characterIDList = []

for char in characters:
    # Names
    for k in ["name"]:
        characterList.append(char[k])
    # IDs
    for k in ["_id"]:
        characterIDList.append(char[k])

# print(characterList)
# print(characterIDList)

# making a key value pair for step 4 of the task 
characterIDPair = zip(characterIDList, characterList)
# use it for step 4 
characterIDDict = dict(characterIDPair)
# print(characterIDDict)
# print(len(characterIDDict))

# # # ------------------------------------------------------------
# # #  Quotes

quoteurl = "https://the-one-api.dev/v2/quote"

quoteResponse = requests.get(quoteurl, headers=headers)
# print(quoteResponse.json())

# # Grabbing just the quotes
# quotesFile = open('quotes.json')
# quotesDict = json.load(quotesFile)

quoteDict = quoteResponse.json()
quotes = quoteDict.get("docs")
quoteList = []

# # for step 4 
quoteMovieIDList = []
quoteCharacterIDList = []

movieTempList = []
charTempList = []

for quote in quotes:
    for k in ["dialog"]:
        quoteList.append(quote[k])
    
    for k in ["movie"]:
        quoteMovieIDList.append(quote[k])
        # experimental for step 4 
        if quote[k] in movieIDDict:
            # movieTempList.append(movieIDDict.values())
            movieTempList.append(movieIDDict[quote[k]])

    for k in ["character"]:
        quoteCharacterIDList.append(quote[k])
        # experimental for step 4
        if quote[k] in characterIDDict:
            charTempList.append(characterIDDict[quote[k]])

# print(movieTempList) 
# print(charTempList)
# print(quoteList)

# # ---------------------------------------------

# Concatenate the three returned JSON files into a single file containing the followings
# 1. The Quote itself
# 2. The name of the character who said the Quote (name field)
# 3. The Movie which the quote is from

# the three final lists: quote (quoteList), character (charTempList) and movie (movieTempList)

finalDict = zip(quoteList, charTempList, movieTempList)
# print(*finalDict)

# answer = [{'quote' : q, 'character' : c, 'movie' : m} for q, c, m in finalDict ]
queryResult = [{'quote' : q, 'character' : c, 'movie' : m} for q, c, m in finalDict ]
# print(type(queryResult))
tempDict = {'docs' : queryResult}
# print(type(tempDict))
jsonQueryResult = json.dumps(tempDict)
# print(type(jsonQueryResult))
# print(jsonQueryResult)


# converting the data to csv file
jsonData = queryResult
# print(jsonData)

jsonKeys = jsonData[0].keys()
with open('lotr.csv', 'w', newline='') as csvFile:
    dict_writer =csv.DictWriter(csvFile, jsonKeys)
    dict_writer.writeheader()
    dict_writer.writerows(jsonData)

# csvFile.close()
# movieFile.close()
# characterFile.close()
# quotesFile.close()
