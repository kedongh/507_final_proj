from flask import Flask, render_template, request

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

@app.route('/search_form', methods=['POST'])
def handle_search_form():
	type = request.form['type']
	location = request.form['loc']
	count = request.form['cnt']
	busi_list = yelp.get_business_list(term=type, location=location, count=count)
	yelp.write_to_business(busi_list)
	yelp.write_to_category(busi_list)

	info_list = []
	for busi in busi_list:
		info = busi.get_business_info()
		info.append(busi.pic)
		info.append(busi.review)
		info_list.append(info)

	return render_template(
		"search_form.html",
		list=info_list,
		count=count
	)

@app.route('/summary_form', methods=['POST'])
def handle_summary_form():
	type = request.form['type']
	location = request.form['loc']
	item = request.form['item']
	order = request.form['order']
	command = [type, location, item, order, '10']
	result = db.process_command(command)

	xvals = []
	yvals = []

	# print(command)

	for res in result:
		xvals.append(res[0])
		if item == 'price':
			yvals.append(res[4])
		if item == 'rating':
			yvals.append(res[3])

	bars_data = go.Bar(
		x = xvals,
		y = yvals
	)

	fig = go.Figure(data=bars_data)
	div = fig.to_html(full_html=False)
	return render_template('summary_form.html',
		plot_div = div
	)


if __name__ == '__main__':
	app.run(debug=True)
