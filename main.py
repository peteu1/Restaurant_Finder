from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    msg = "Welcome to the launch page for my restaurant finder."
    # TODO: Add more information (move to text file)
    # TODO: Link to application
    return msg

@app.route("/restaurant_finder")
def restaurant_finder():
    # TODO
    return "This will be the app."

if __name__ == "__main__":
    app.run(debug=True)
