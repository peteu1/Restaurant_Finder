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
        self.location_received = "0"  # TODO: Render everything but map, then load map when location is requested and receieved. Combine with _templated_rendered
        self._template_rendered = False

    def setLatLon(self, lat, lon):
        self.center_long = lon
        self.center_lat = lat
        self.location_received = "1"

    def collect_data(self, results, reviews, selected_idx="0"):
        # Add corresp. reviews to each business "result"
        combined_results = results
        for _, review in enumerate(reviews):
            combined_results[_]["reviews"] = review['reviews']
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


# @app.route("/getLocation", methods=['POST', 'GET'])
# def test_post():
#     print("Test method:", request.method)
#     if request.method == 'POST':
#         data = request.get_json()
#         print("Received:", data)
#         lat = data["lat"]
#         lon = data["lon"]
#         print("location received:", lat, lon)
#         storedData.setLatLon(lat, lon)
#         # Get results from API and load app.html
#         # results, reviews = restaurants.reload_results()
#         # storedData._template_rendered = True
#         # return render_template("app.html", **storedData.collect_data(results, reviews))
#         # TODO: Call background_process()
#         return redirect(url_for("background_process")) # restaurant_finder

#     return render_template("home.html")

@app.route("/", methods=['POST', 'GET'])
def restaurant_finder():
    print(">restaurant_finder() called")
    return render_template("home.html")


food_selection_map = {
    "0": "Select Style",
    "1": "Italian",
    "2": "Brazilian",
    "3": "American",
    "4": "Chinese",
    "5": "Japanese",
    "6": "Bar",
}

@app.route('/restaurant_finder', methods=['POST', 'GET'])
def background_process():
    print("> background_process() called")
    args = request.args
    print("Data:", args)
    if storedData.location_received == "0":
        print("Setting location..")
        lat, lon = float(args["lat"]), float(args["lon"])
        storedData.setLatLon(lat, lon)
        results, reviews = restaurants.set_location(lat, lon)
        storedData._template_rendered = True
        return render_template("app.html", **storedData.collect_data(results, reviews))

    if request.method == 'POST':
        data = request.get_json()
        print("Received:", data)  # TODO: Search term not working properly
        # TODO: Properly track these and toggle values
        cheap = 0
        pricey = 0
        if 'cheap' in data.keys():
            print("Cheap clicked!")
            cheap = 1
        if 'pricey' in data.keys():
            print("Pricey clicked!")
            pricey = 1
        results, reviews = restaurants.update_excluded_prices(cheap, pricey)
    else:
        results, reviews = restaurants.reload_results()
    # food_idx = args['sel_food_type']
    # if food_idx != "0":
    #     food_name = food_selection_map[food_idx]
    #     print("Food selection:", food_name)
    #     results, reviews = restaurants.set_meal(food_name)
    
    print("New length:", len(results))
    print("Filter pricey:", restaurants.filter_pricey)
    print("Filter cheap:", restaurants.filter_cheap)
    print("All length", len(restaurants.all_results))
    
    return render_template("app.html", **storedData.collect_data(results, reviews))
    #return render_template("app.html", **storedData.collect_data(results, reviews, food_idx))
    


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000, debug=False)
