from flask import Flask, request, jsonify, render_template, redirect, url_for
from scripts.Yelp_API import Restaurants
from scripts import creds
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfu089jasdmfoim21f0'
bootstrap = Bootstrap(app)
moment = Moment(app)
food_map = {
    "0": "Select Style",
    "1": "Italian",
    "2": "Brazilian",
    "3": "American",
    "4": "Chinese",
    "5": "Japanese",
    "6": "Bar",
}

class SearchForm(FlaskForm):
    selectedTerm = SelectField(u"What type of food?  Select from dropdown", choices=[(key, food_map[key]) for key in food_map])
    term = StringField("Or search:") # , validators=[DataRequired()]
    submit = SubmitField('Submit')

class ButtonForm(FlaskForm):
    cheap = BooleanField("Nothing\nCheap")


class StoredData():
    def __init__(self):
        # TODO: centers will come from user location
        self.zoom = 12
        self.center_long = -80.4137  # Blacks
        self.center_lat = 37.22922  # Burg  (You know location isn't working if it shows bburg)
        self.location_received = "0"  # TODO:  Combine with _templated_rendered
        self._template_rendered = False
        self.term = "dinner"
        self.filter_cheap = 0
        self.filter_pricey = 0

    def setLatLon(self, lat, lon):
        self.center_long = lon
        self.center_lat = lat
        self.location_received = "1"

    def collect_data(self, results, reviews, term, searchForm):
        #results = reviews = [] # TODO: Remove
        # Add corresp. reviews to each business "result"
        combined_results = results
        for _, review in enumerate(reviews):
            combined_results[_]["reviews"] = review['reviews']
        return {
            'center_long': self.center_long,
            'center_lat': self.center_lat,
            'zoom': self.zoom,
            'searchForm': searchForm,
            'term': term,
            'cheap': bool(self.filter_cheap),
            'pricey': bool(self.filter_pricey),
            'location_received': self.location_received,
            'results': combined_results
        }
        #'results': combined_results,
            # 'selected_idx': selected_idx,


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# class Restaurants():
#     def __init__(self):
#         self.meal = "dinner"
#         self.filter_cheap = self.filter_pricey = False
    
#     def update_search_terms(self, cheap=-1, pricey=-1, term=None):
#         """Filters results based on price without making call to API.
#         Returns:
#             filtered_results (list): all_results filtered by price
#             filtered_reviews (list): all_reviews filtered by price (aligns with results)
#         """
#         print("\n\n> !!!update_search_terms() called", cheap, pricey, term)
#         self.meal = term

#         return "a", "b"


storedData = StoredData()

@app.route("/", methods=['POST', 'GET'])
def restaurant_finder():
    print(">restaurant_finder() called")
    return render_template("home.html")

@app.route('/restaurant_finder', methods=['GET', 'POST'])
def index():
    term = storedData.term
    searchForm = SearchForm()
    args = request.args
    print("Data:", args)
    print("Method:", request.method)
    print("searchForm.validate_on_submit()", searchForm.validate_on_submit())
    
    if storedData.location_received == "0":
        print("Setting location..")
        lat, lon = float(args["lat"]), float(args["lon"])
        storedData.setLatLon(lat, lon)
        if 'restaurants' not in globals():
            global restaurants
            restaurants = Restaurants(lat, lon)
            print("\n\n> Creating restaurants class\n")
            results, reviews = restaurants.reload_results()
            # results, reviews = restaurants.update_search_terms(
            #     storedData.filter_cheap,
            #     storedData.filter_pricey, 
            #     storedData.term
            # )
            # TODO: Remove above
            kwargs = storedData.collect_data(results, reviews, term, searchForm)
    if request.method == "POST":
        print("KJLDASKF:", request.form)
        if searchForm.validate_on_submit():
            # Get entered search term
            term = searchForm.term.data
            print("term", term)
            selected = searchForm.selectedTerm.data
            print("selected:", selected)
            if term == "" and int(selected) > 0:
                term = food_map[selected]
            _term = term

        else:
            _term = None
            if 'cheap' in request.form:
                print("Cheap:", request.form['cheap'])
                if request.form['cheap'] == 'on':
                    storedData.filter_cheap = 0
                else:
                    storedData.filter_cheap = 1
            if 'pricey' in request.form:
                print("pricey:", request.form['pricey'])
                if request.form['pricey'] == 'on':
                    storedData.filter_pricey = 0
                else:
                    storedData.filter_pricey = 1

        # Update results if term changed
        if term != storedData.term:
            storedData.term = term
        results, reviews = restaurants.update_search_terms(
            storedData.filter_cheap,
            storedData.filter_pricey,
            _term
        )
        kwargs = storedData.collect_data(results, reviews, term, searchForm)
    else:
        # Method = Get
        #results, reviews = restaurants.filtered_results, restaurants.filtered_reviews
        # TODO
        # results = reviews = []
        kwargs = storedData.collect_data(results, reviews, term, searchForm)
    
    return render_template('index.html', **kwargs)





if __name__ == '__main__':
    app.run(threaded=True, port=5001, debug=False)
