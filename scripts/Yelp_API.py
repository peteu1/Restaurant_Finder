import sys
import os
import json
import pprint
import requests
import urllib
from yelp.client import Client
from scripts import creds # TODO
#import creds


API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
API_KEY = creds.API_Key

# Defaults for our simple example.
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'Blacksburg, VA'
DEFAULT_LIMIT = 4 # TODO


class Yelp():
    def __init__(self, API_KEY):
        """
        Args:
            API_KEY (str): my Yelp API key
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

    def search(self, term, search_limit, location, coords):
        """Query the Search API by a search term and location.
        Args:
            term (str): The search term passed to the API.
            location (str): The search location passed to the API.
        Returns:
            dict: The JSON response from the request.
        """
        url_params = {
            'term': term.replace(' ', '+'),
            'limit': search_limit,
        }
        if coords != (0,0):
            url_params['latitude'], url_params['longitude'] = coords
        else:
            url_params['location'] = location.replace(' ', '+')
        return self.request(API_HOST, SEARCH_PATH, url_params=url_params)

    def get_business(self, business_id):
        """Query the Business API by a business ID.
        Args:
            business_id (str): The ID of the business to query.
        Returns:
            dict: JSON response from request for more business details
            dict: JSON response from reviews request for business_id
        """
        business_path = BUSINESS_PATH + business_id
        biz_reviews_path = business_path + "/reviews"
        return self.request(API_HOST, business_path), self.request(API_HOST, biz_reviews_path)

    def query_api(self, term, search_limit=DEFAULT_LIMIT, location="Blacksburg VA", coords=(0,0)):
        """Queries the API by the input values from the user.
        Args:
            term (str): The search term to query.
            location (str): The location of the business to query.
        Returns:
            (bool): False if no results were found.
        """
        response = self.search(term, search_limit, location, coords)
        businesses = response.get('businesses')
        results = []
        if not businesses:
            print(f"No businesses for {term} in {location} found.")
            return results
        print(f"{len(businesses)} businesses found.")
        return businesses


class Restaurants():
    def __init__(self, lat, lon):
        self.yelp = Yelp(creds.API_Key)
        self.coords = (lat, lon)
        self.location = "Blacksburg, VA"  # TODO: Let user type location if get location fails
        self.meal = "dinner"  # Search term
        self.all_businesses = []
        self.all_results = self.all_reviews = []
        self.filtered_results = self.filtered_reviews = []
        self.filter_cheap = self.filter_pricey = False
        self.num_results = 4  # TODO

    def reload_results(self):
        self.all_businesses = self.yelp.query_api(self.meal, self.num_results, self.location, self.coords)
        # Get more information for each business that matches current filters
        self.all_results = []
        self.all_reviews = []
        # TODO: Only load those displayed/top 5 at a time?
        for business in self.all_businesses:
            business_id = business['id']
            response, reviews = self.yelp.get_business(business_id)
            # Only add to all_results if there is location data
            if 'coordinates' in response:
                # Modify photo url to direct to yelp
                #if 'image_url' in response: TODO
                img_ID = os.path.basename(os.path.dirname(response['image_url']))
                response['all_photos'] = f"https://www.yelp.com/biz_photos/{response['alias']}?select={img_ID}"
                print("Adding:", response['name'])
                self.all_results.append(response)
                self.all_reviews.append(reviews)
        self.filtered_results = self.all_results
        self.filtered_reviews = self.all_reviews
        #filtered_results, filtered_reviews = self.update_excluded_prices()
        #return filtered_results, filtered_reviews
        return self.all_results, self.all_reviews

    def update_search_terms(self, cheap=-1, pricey=-1, term=None):
        """Filters results based on price without making call to API.
        Returns:
            filtered_results (list): all_results filtered by price
            filtered_reviews (list): all_reviews filtered by price (aligns with results)
        """
        print("\n\n> update_search_terms() called", cheap, pricey, term)
        if term != self.meal and term != None:
            self.meal = term
            print("> Setting self.meal to:", term)
            # Reload results
            all_results, all_reviews = self.reload_results()
        else:
            all_results = self.all_results.copy()
            all_reviews = self.all_reviews.copy()
        
        self.filter_cheap = bool(cheap)
        self.filter_pricey = bool(pricey)
        if self.filter_cheap or self.filter_pricey:
            # Filter price
            filtered_results = []
            filtered_reviews = []
            for result, review in zip(self.all_results, self.all_reviews):
                if "price" in list(result.keys()):
                    print("Price:", result['price'])
                    price_level = len(result['price'])
                    if (self.filter_cheap and price_level <= 1) or (self.filter_pricey and price_level >= 3):
                        pass
                    else:
                        filtered_results.append(result)
                        filtered_reviews.append(review)
                else:  # No price level, add regardless
                    filtered_results.append(result)
                    filtered_reviews.append(review)
        else:  # No price filters, use all results
            filtered_results = all_results
            filtered_reviews = all_reviews
        # Store filtered list and return
        self.filtered_results = filtered_results
        self.filtered_reviews = filtered_reviews
        return filtered_results, filtered_reviews
# End restaurants Class
