from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route('/')
def home():
    mars_dict= mongo.db.mars_dict.find_one()
    return render_template('index.html', mars=mars_dict)
    


@app.route('/scrape')
def scrape():
    mars_dict = mongo.db.mars_dict
    data = scrape_mars.scrape()
    mars_dict.update({},data,upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)