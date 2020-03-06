# app.py
from flask import Flask, request, jsonify, render_template, redirect, url_for
from scripts.Yelp_API import Restaurants
from scripts import creds


class StoredData():
    def __init__(self):
        # TODO: centers will come from user location
        self.zoom = 12
        self.center_long = -80.4137  # Blacks
        self.center_lat = 37.22922  # Burg  (You know location isn't working if it shows bburg)
        self.location_received = "0"  # TODO: This could be combined with _templated_rendered variable. Both effect code same way
        self._template_rendered = False

    def collect_data(self, results, reviews, selected_idx=0):
        # Add corresp. reviews to each business "result"
        combined_results = results
        print('len res', len(results))
        print('len rev', len(reviews))
        for _, review in enumerate(reviews):
            combined_results[_]["reviews"] = review['reviews']
        if len(reviews):
            print(results[0])
            print(reviews[0])
        return {
            'center_long': self.center_long,
            'center_lat': self.center_lat,
            'zoom': self.zoom,
            'location_received': self.location_received,
            'results': combined_results,
            'selected_idx': selected_idx,
        }

app = Flask(__name__)
restaurants = Restaurants()
storedData = StoredData()


@app.route("/test", methods=['POST'])
def test_post():
    if request.method == 'POST':
        names = request.get_json()
        for name in names:
            print("Param received:", name)
        return '', 200

@app.route("/")
def restaurant_finder():
    restaurants.reload_results()
    results = restaurants.all_results
    reviews = restaurants.all_reviews
    print("Len orig:", len(results))
    print("results:", results[0])
    storedData._template_rendered = True
    return render_template("app.html", **storedData.collect_data(results, reviews))


food_selection_map = {
    "0": "Select Style",
    "1": "Italian",
    "2": "Brazilian",
    "3": "American",
    "4": "Chinese",
    "5": "Japanese",
    "6": "Bar",
}

@app.route('/restaurant_finder')
def background_process():
    if not storedData._template_rendered:
        restaurants.reload_results()
    args = request.args
    print("Data:", args)
    results, reviews = restaurants.update_excluded_prices(int(args['cheap']), int(args['pricey']))
    # TODO: Implement option in html to view the reviews (max 3)
    food_idx = args['sel_food_type']
    if food_idx != "0":
        food_name = food_selection_map[food_idx]
        print("Food selection:", food_name)
        results, reviews = restaurants.set_meal(food_name)
    
    print("New length:", len(results))
    print("Filter pricey:", restaurants.filter_pricey)
    print("Filter cheap:", restaurants.filter_cheap)
    print("All length", len(restaurants.all_results))
    
    return render_template("app.html", **storedData.collect_data(results, reviews, food_idx))
    


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000, debug=True)
