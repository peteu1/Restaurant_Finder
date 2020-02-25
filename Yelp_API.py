import sys
import json
import pprint
import requests
import urllib
from yelp.client import Client
import creds


API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
API_KEY = creds.API_Key

# Defaults for our simple example.
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'Blacksburg, VA'
DEFAULT_LIMIT = 4


class Yelp():
    def __init__(self, API_KEY):
        """
        Args:
            API_KEY (str): 
        """
        self.API_KEY = API_KEY
        self.client = Client(self.API_KEY)

    def request(self, host, path, url_params=None):
        """Given your API_KEY, send a GET request to the API.
        Args:
            host (str): The domain host of the API.
            path (str): The path of the API after the domain.
            url_params (dict): An optional set of query parameters in the request.
        Returns:
            dict: The JSON response from the request.
        Raises:
            HTTPError: An error occurs from the HTTP request.
        """
        url_params = url_params or {}
        url = f"{host}{urllib.parse.quote(path.encode('utf8'))}"
        headers = {'Authorization': f'Bearer {self.API_KEY}'}
        response = requests.request('GET', url, headers=headers, params=url_params)
        return response.json()

    def search(self, term, location, search_limit):
        """Query the Search API by a search term and location.
        Args:
            term (str): The search term passed to the API.
            location (str): The search location passed to the API.
        Returns:
            dict: The JSON response from the request.
        """
        url_params = {
            'term': term.replace(' ', '+'),
            'location': location.replace(' ', '+'),
            'limit': search_limit
        }
        return self.request(API_HOST, SEARCH_PATH, url_params=url_params)

    def get_business(self, business_id):
        """Query the Business API by a business ID.
        Args:
            business_id (str): The ID of the business to query.
        Returns:
            dict: The JSON response from the request.
        """
        business_path = BUSINESS_PATH + business_id
        return self.request(API_HOST, business_path)

    def query_api(self, term, location, search_limit=DEFAULT_LIMIT):
        """Queries the API by the input values from the user.
        Args:
            term (str): The search term to query.
            location (str): The location of the business to query.
        Returns:
            (bool): False if no results were found.
        """
        response = self.search(term, location, search_limit)
        businesses = response.get('businesses')
        results = []
        if not businesses:
            print(f"No businesses for {term} in {location} found.")
            return results
        print(f"{len(businesses)} businesses found.")
        
        # TODO: Loop through all results
        for business in businesses:
            business_id = business['id']
            response = self.get_business(business_id)
            if 'coordinates' in response:
                print("Adding:", response['name'])
                results.append(response)
            #pprint.pprint(response, indent=2)
        return results


#def main():

term = DEFAULT_TERM             # help='Search term (default: %(default)s)'
location = DEFAULT_LOCATION     # help='Search location (default: %(default)s)'

yelp = Yelp(API_KEY)
results = yelp.query_api(term, location)  # search_limit

print("\n\nResults:\n")
#print(results)

