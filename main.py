import requests
import os
from pprint import pprint as pp #
import pymongo
from pymongo import MongoClient


def get_api():
    url_api = 'https://www.swapi.tech/api/starships/'
    responses = []
    response = requests.get(url_api).json() # converts request to json file
    responses += response['results'] # add only results key
    while response['next'] is not None:  # collect data on all pages until none
        response = requests.get(response['next']).json()  # all pages by next
        responses += response['results']  # all pages included
    return responses

# responses = get_api()
# pp(responses)

def collect_starships():
    starships = []
    for starship in get_api():
        starships.append(requests.get(starship['url']).json()['result']['properties'])
    return starships

# starships = collect_starships()
# pp(starships)

def collect_pilots():
    starships = []
    for starship in collect_starships():
        pilots = []
        for pilot in starship['pilots']:
            pilots.append(requests.get(pilot).json()['result']['properties']['name'])
            # names of the pilots
        starship.update({'pilots': pilots})  # replaces the pilot list with a list of character names
        starships.append(starship)
    return starships

#pp(collect_pilots())
# Loading files to Mongodb Database

client = pymongo.MongoClient()
db = client["StarWars"]

def load_data_directly():
    db['starships'].drop() # droping collection if exist
    for starship in collect_pilots():
        db.starships.insert_one(starship) # creating a starship collections

if __name__=="__main__":
    pass
    load_data_directly()
