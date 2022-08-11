""" <!-- This project will take you through the process of mashing up data from two different APIs to make movie recommendations.
The TasteDive API lets you provide a movie (or bands, TV shows, etc.) as a query input, and returns a set of related items.
The OMDB API lets you provide a movie title as a query input and get back data about the movie, including scores from various review sites (Rotten Tomatoes, IMDB, etc.).

You will put those two together. You will use TasteDive to get related movies for a whole list of titles. The documentation for the API is at https://tastedive.com/read/api.

Define a function, called get_movies_from_tastedive. It should take one input parameter, a string that is the name of a movie or music artist. The function should return the 5 TasteDive results that are associated with that string; be sure to only get movies, not other kinds of media. It will be a python dictionary with just one key, ‘Similar’.

Try invoking your function with the input “Black Panther”.

 """

import requests_with_caching
import json

def get_movies_from_tastedive(s):
    baseurl = "https://tastedive.com/api/similar"
    params_diction = {}
    params_diction ["q"] = s
    params_diction ["type"] = "movies"
    params_diction ["limit"] = "5"
    resp = requests_with_caching.get(baseurl, params = params_diction)
    #print(json.dumps(resp), indent = 2)
    return resp.json()
#get_movies_from_tastedive("Black Panther")

"""
Next, you will need to write a function that extracts just the list of movie titles from a dictionary 
returned by get_movies_from_tastedive. Call it extract_movie_titles.
 """
def extract_movie_titles(get_movies_from_tastedive):
    dct = get_movies_from_tastedive
    lst = dct['Similar']['Results']
    return [d['Name'] for d in lst]
#print(extract_movie_titles(get_movies_from_tastedive("Black Panther")))

""" 
Next, you’ll write a function, called get_related_titles. It takes a list of movie titles as input. 
It gets five related movies for each from TasteDive, extracts the titles for all of them, and combines 
them all into a single list. Don’t include the same movie twice.
 """
def get_related_titles(movies):
    lst1 = []
    for m in movies:
        for d in extract_movie_titles(get_movies_from_tastedive(m)):
            if d not in lst1:
                lst1 = lst1 + [d]
    return lst1

""" Your next task will be to fetch data from OMDB. The documentation for the API is at https://www.omdbapi.com/

Define a function called get_movie_data. It takes in one parameter which is a string that should represent 
the title of a movie you want to search. The function should return a dictionary with information about that movie.

Again, use requests_with_caching.get(). For the queries on movies that are already in the cache, 
you won’t need an api key. You will need to provide the following keys: t and r. As with the TasteDive cache, 
be sure to only include those two parameters in order to extract existing data from the cache.
 """
def get_movie_data(str_movie):
    baseurl = "http://www.omdbapi.com/"
    params_diction = {}
    params_diction ['t'] = str_movie
    params_diction ['r'] = "json"
    resp = requests_with_caching.get(baseurl, params = params_diction)
    #print(resp.text[:150])
    return resp.json()
#print(get_movie_data("Deadpool 2"))

"""
Now write a function called get_movie_rating. It takes an OMDB dictionary result for one movie and extracts the 
Rotten Tomatoes rating as an integer. For example, if given the OMDB dictionary for “Black Panther”, 
it would return 97. If there is no Rotten Tomatoes rating, return 0.
 """
def get_movie_rating(get_movie_data):
    d = get_movie_data
    rt = d['Ratings']
    val = 0
    for dct in rt:
        if dct['Source'] == 'Rotten Tomatoes':
            val = val + int(dct['Value'].strip("%"))
            break
        else:
            val = 0
    return val

#print(get_movie_rating(get_movie_data("Deadpool 2")))

""" Define a function get_sorted_recommendations. It takes a list of movie titles as an input. 
It returns a sorted list of related movie titles as output, up to five related movies for each input movie title. 
The movies should be sorted in descending order by their Rotten Tomatoes rating, as returned by the get_movie_rating 
function. Break ties in reverse alphabetic order, so that ‘Yahşi Batı’ comes before ‘Eyyvah Eyvah’.
 """
def get_sorted_recommendations(movies):
    movie_list = get_related_titles(movies)
    
    new_list = sorted(movie_list, key = lambda m : -(get_movie_rating(get_movie_data(m))))
    return new_list
