# app.py
from flask import Flask, request, jsonify, render_template, redirect, url_for
from scripts.Yelp_API import Restaurants
from scripts import creds


class StoredData():
    def __init__(self):
        # TODO: centers will come from user location
        self.center_long = -80.4137
        self.center_lat = 37.22922
        self.zoom = 12

    def collect_data(self, results, selected_idx=0):
        return {
            'center_long': self.center_long,
            'center_lat': self.center_lat,
            'zoom': self.zoom,
            'results': results,
            'selected_idx': selected_idx,
        }

app = Flask(__name__)
restaurants = Restaurants()
storedData = StoredData()


@app.route("/") #, methods=['GET', 'POST']
def restaurant_finder():
    restaurants.reload_results()
    results = restaurants.all_results
    print("Len orig:", len(results))
    #a = request.form.getlist("money")
    #print("a:", a)
    return render_template("app.html", **storedData.collect_data(results))


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
    args = request.args
    print("Data:", args)
    results = restaurants.update_excluded_prices(int(args['cheap']), int(args['pricey']))

    food_idx = args['sel_food_type']
    if food_idx != "0":
        food_name = food_selection_map[food_idx]
        print("Food selection:", food_name)
        results = restaurants.set_meal(food_name)
    
    print("New length:", len(results))
    print("Filter pricey:", restaurants.filter_pricey)
    print("Filter cheap:", restaurants.filter_cheap)
    print("All length", len(restaurants.all_results))
        
    return render_template("app.html", **storedData.collect_data(results, food_idx))
    


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
