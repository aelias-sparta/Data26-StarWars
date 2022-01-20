import unittest
from unittest.mock import patch
from main import StarWarsData
p = StarWarsData(url='https://www.swapi.tech/api/starships/')

#testing all my elements in the requests are strings

class TestMain(unittest.TestCase):

    def test_get_api(self):
        for req in p.get_api():
            assert type(req['name']) is str

    def test_collect_starships(self):
        for name in p.collect_starships():
            assert type(name['name']) is str

    def test_collect_pilots(self):
        for pilot in p.collect_pilots():
            for name in pilot['pilots']:
                assert type(name) is str

if __name__ == '__main__':
    unittest.main()