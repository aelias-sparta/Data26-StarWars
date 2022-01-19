import requests
import os
from pprint import pprint as pp #
import pymongo
from pymongo import MongoClient

class StarWarsData():

    def __init__(self, url):
        self.url = url
        self.client = pymongo.MongoClient()
        self.db = self.client["StarWars"]

    def get_api(self):
        responses = []
        response = requests.get(self.url).json() # converts request to json file
        responses += response['results'] # add only results key
        while response['next'] is not None:  # collect data on all pages until none
            response = requests.get(response['next']).json()  # all pages by next
            responses += response['results']  # all pages included
        return responses

    def collect_starships(self):
        starships = []
        for starship in self.get_api():
            starships.append(requests.get(starship['url']).json()['result']['properties'])
        return starships

    def collect_pilots(self):
        starships = []
        for starship in self.collect_starships():
            pilots = []
            for pilot in starship['pilots']:
                pilots.append(requests.get(pilot).json()['result']['properties']['name'])
                # names of the pilots
            starship.update({'pilots': pilots})  # replaces the pilot list with a list of character names
            starships.append(starship)
        return starships

    def load_data_directly(self):
        self.db['starships'].drop() # droping collection if exist
        for starship in self.collect_pilots():
            self.db.starships.insert_one(starship) # creating a starship collections

if __name__=="__main__":

    url_api = 'https://www.swapi.tech/api/starships/'
    starwarsObject = StarWarsData(url=url_api)
    starwarsObject.load_data_directly()
