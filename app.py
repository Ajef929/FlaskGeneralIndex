from flask import Flask, render_template, request, redirect, url_for, session
from typing import Dict
from search import search
import pandas as pd
import os


app = Flask(__name__)
app.secret_key = "#$%#$%^%^BFGBFGBSFGNSGJTNADFHH@#%$%#T#FFWF$^F@$F#$FW"
IMG_FOLDER = os.path.join('static', 'IMG')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/search", methods=["POST", "GET"])
def searcht():
	if request.method == "POST":
		query = request.form["query"]
		search_within = request.values.get("type")
		start_year = request.values.get("start")
		end_year = request.values.get("end")
		export = request.values.get("export_check")
		results, info = search(query, search_within, start_year, end_year, export)
		year_plot_1 = os.path.join(app.config['UPLOAD_FOLDER'], 'year_plot1.png')
		year_plot_2 = os.path.join(app.config['UPLOAD_FOLDER'], 'year_plot2.png')
	return render_template("search.html", results=results, info=info, query=query,total_results=len(results),year_plot_1=year_plot_1,year_plot_2=year_plot_2)

if __name__ == '__main__':
	app.run(debug=True, host="132.181.102.8")
