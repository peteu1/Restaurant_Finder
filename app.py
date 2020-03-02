# app.py
from flask import Flask, request, jsonify, render_template
from Yelp_API import Yelp
import creds


app = Flask(__name__)


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
# End restaurants Class

restaurants = Restaurants()


@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)


@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })


# A welcome message to test our server
@app.route('/')
def index():
    # TODO
    return render_template("home.html")
    #return "<h1>Welcome to our server !!</h1>"


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



if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)