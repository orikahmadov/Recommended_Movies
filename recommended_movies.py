import json
import requests

#This function is taking a movie name as its parameters and sends the request to the api and
# returns 5 movies and stores them in movies variable
def get_movies_from_tastedive(movie_name,api_key =  "[Your Api KEY]"):
    parameters = {"q": movie_name, "type": "movies", "limit": 5, "k" : api_key}
    result = requests.get("https://tastedive.com/api/similar", params=parameters).json()
    movies = result
    return movies


#This function takes the get_movies_from_tastedive function as parameter and extracts the movie titles from each
# movie and stores them
def extract_movie_titles(func):
    movie_titles = [movie["Name"] for movie in func["Similar"]["Results"]]
    return movie_titles


#This function takes list of movies as parameter and iterates through the previous 2 datas
#if movie title is not already in the list of extracted movies and stores it in related_movies variable
def get_related_titles(list_of_movie_title):
    related_movies = list()
    for title in list_of_movie_title:
        movies_from_tastedive = get_movies_from_tastedive(title)
        movies_from_extract = extract_movie_titles(movies_from_tastedive)
        for movie in movies_from_extract:
            if movie not in related_movies:
                related_movies.append(movie)
    return related_movies

#This function takes movie name as param and sends get request to another API OMDBAPI
#returns json
def get_movie_data(movie_name):
    parameters = {'t': movie_name, 'r': 'json'}
    api_result_omdp = requests.get('http://www.omdbapi.com/?i=[Your Api KEY]', params=parameters).json()
    res = api_result_omdp
    return res



#This movie takes previous function as param and extracts the Rotten tomatoes rating of given movie and stores
#its value as integer in variable
def get_movie_raiting(movieName):
    movie =  get_movie_data(movieName)
    rotten_tomatoes_raiting = 0
    for i in movie["Ratings"]:
        if i["Source"] == "Rotten Tomatoes":
            rotten_tomatoes_raiting +=(int(i["Value"][:2]))
    else:
            rotten_tomatoes_raiting += 0
    return  rotten_tomatoes_raiting


#This function takes list of movie titles then it returns five related movies for each movie it finds the
# "Rotten Tomatoes" score and then sorts them by their score in dictionary data type of Python3 <3
def sorted_recommendations(list_of_titles):
    movie_titles = [movie for movie in list_of_titles]
    related_movies = []
    scores = []
    for i in get_related_titles(movie_titles):
        related_movies.append(i)
        scores.append(get_movie_raiting(i))
    movies_and_scores = dict(zip(related_movies,scores))
    sorted_movies = sorted(movies_and_scores.items(), key= lambda movie : movie[1], reverse=True)
    result = [(movie,score) for (movie,score) in sorted(movies_and_scores.items(), key = lambda x : x[1],reverse=True) ]
    return result

def writeMoviestoFile():
   import time
   finished =  False
   while not finished:
       askForMovie = input("Please enter at least 2 movie names  and separate them with space: ")
       print("\n")
       finished =  False
       found_movies = []
       movies_separated =  askForMovie.split()
       if not askForMovie:
           print("No movie name is given ")
           finished =  False
       else:
           for movie in sorted_recommendations(movies_separated):
               print(movie)
               found_movies.append(movie)
               finished = True

   else:
       print("\n")
       print("All movies are listed")
       with open("movies.txt", "w")  as file:
           file.writelines(str(found_movies))
           file.write("\n")

writeMoviestoFile()


#I have written all these scripts by mysels Coursera has motivated me to do this project
#Orkhan Ahmadov
