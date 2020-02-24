from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    # TODO: Add more information to home.html
    # TODO: Link to application
    return render_template("home.html")

@app.route("/restaurant_finder")
def restaurant_finder():
    # TODO
    return render_template("app.html")

if __name__ == "__main__":
    app.run(debug=True)
