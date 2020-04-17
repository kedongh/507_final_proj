from flask import Flask, render_template

import yelp
import db
import scrape
import sqlite3
import plotly.graph_objects as go


app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search')
def search():
	return render_template('search.html')

@app.route('/summary')
def summary():
	return render_template('summary.html')


if __name__ == '__main__':
	app.run(debug=True)