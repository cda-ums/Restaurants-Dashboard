from flask import Flask, render_template, Blueprint
from flask_pymongo import PyMongo
import chartkick
import time
import pymongo

app = Flask(__name__)
mongo = PyMongo(app)

ck = Blueprint('ck_page', __name__, static_folder=chartkick.js())
app.register_blueprint(ck, url_prefix='/ck')
app.jinja_env.add_extension("chartkick.ext.charts")


@app.route('/')
def home_page():
    restaurants = mongo.db.restaurants.find({})
    data = {}

    for r in restaurants:
    	data[r['borough']] = data.get(r['borough'], 0) + 1

    
    return render_template('index.html', data=data)
    #return restaurant['name']

@app.route('/cuisine')
def cuisine_page():
    #borough1 = mongo.db.restaurants.find({"borough": "Queens"})
    restaurants = mongo.db.restaurants.find({})
    data = {}

    for r in restaurants:
    	data[r['cuisine']] = data.get(r['cuisine'], 0) + 1

    
    return render_template('cuisine.html', data=data)
    #return restaurant['name']

@app.route('/score')
def score_page():
	restaurants = mongo.db.restaurants.find({})
	data = {}

	for r in restaurants:
		grades = r['grades']
		avg_score = 0
		count = 0
		for g in grades:
			if g['score'] is not None:
				avg_score += g['score']
				count += 1
		if count != 0:
			avg_score = avg_score / count
		data[str(avg_score)] = data.get(str(avg_score), 0) + 1

	return render_template('score.html', data=data)