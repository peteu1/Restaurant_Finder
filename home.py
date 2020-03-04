# app.py
from flask import Flask, request, jsonify, render_template, redirect, url_for
from scripts.Yelp_API import Restaurants
from scripts import creds


class StoredData():
    def __init__(self):
        # TODO: Compute center automatically
        self.center_long = -80.4137
        self.center_lat = 37.22922
        self.zoom = 10

    def collect_data(self, results):
        return {
            'center_long': self.center_long,
            'center_lat': self.center_lat,
            'zoom': self.zoom,
            'results': results,
        }

app = Flask(__name__)
restaurants = Restaurants()
storedData = StoredData()


@app.route('/')
def index():
    return render_template("home.html")


@app.route("/restaurant_finder") #, methods=['GET', 'POST']
def restaurant_finder():
    restaurants.reload_results()
    results = restaurants.filtered_results
    #a = request.form.getlist("money")
    #print("a:", a)
    return render_template("app.html", **storedData.collect_data(results))


@app.route('/background_process', methods = ['GET', 'POST'])
def background_process():
    print("Data:", request.data)
    return request.data
    # exclude = request.args['exclude']
    # print("Clicked!!", exclude)
    # prev_results = restaurants.filtered_results
    # new_results = restaurants.update_excluded_prices(exclude)
    # print("Excluding:", restaurants.exclude_prices)
    # print("Len old:", len(prev_results))
    # print("Len new:", len(new_results))
    # if len(new_results) != len(prev_results):
    #     print("Length changed!")
    #     return redirect(url_for("static", filename="app", **storedData.collect_data(new_results)))
    # return ("nothing")


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
