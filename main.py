from flask import Flask, render_template
from Yelp_API import Yelp
import creds


app = Flask(__name__)

@app.route("/")
def home():
    # TODO: Add more information to home.html
    # TODO: Link to application
    return render_template("home.html")


class Restaurants():

    def __init__(self):
        self.yelp = Yelp(creds.API_Key)
        self.location = "Blacksburg, VA"  # TODO: Get automatically
        self.meal = "dinner"
        self.all_results = []
        self.filtered_results = []
        self.min_price = 1
        self.max_price = 4
        self.num_results = 4  # TODO

    def reload_results(self):
        self.all_results = self.yelp.query_api(self.meal, self.location, self.num_results)
        self.filter_price(self.min_price, self.max_price)

    def set_meal(self, meal):
        self.meal = meal
        # TODO: Filter hours?
        self.reload_results()

    def filter_price(self, min_price, max_price):
        self.min_price = min_price
        self.max_price = max_price
        if self.min_price == 1 and self.max_price == 4:
            self.filtered_results = self.all_results
            return None
        # Filter on price and remove restaurants with unknown prices
        self.filtered_results = []
        for result in self.all_results:
            if "price" in result.keys():
                price_level = len(result.price)
                if price_level > min_price and price_level < max_price:
                    self.filtered_results.append(result)


@app.route("/restaurant_finder")
def restaurant_finder():
    restaurants.reload_results()
    results = restaurants.filtered_results
    # TODO: Compute center automatically
    kwargs = {
        'center_long': -80.4137,
        'center_lat': 37.22922,
        'zoom': 10,
        'results': results,
    }
    return render_template("app.html", **kwargs)

if __name__ == "__main__":
    global restaurants
    restaurants = Restaurants()
    app.run(debug=True)
