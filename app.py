from flask import Flask, request, render_template
import json
import requests


API_URL = 'https://rickandmortyapi.com/api/character'
 
#
def call_api(url, params):
    # url = 'https://rickandmortyapi.com/api/character'
    response = requests.get(url=url, params=params)
    try:
        response_dict = response.json()
        return response_dict
    except Exception as e:
        print(e)
# 




app = Flask(__name__)

@app.route("/")
def index():
    page = request.args.get('page', 1)
    response = call_api(API_URL, params={'page':2})
    s = "<h1>Hello there ...</h1>"
    for r in response["results"]:
        s+=f"\n<h2> <a href={r["image"]}>{r["name"]}</a></h2>"
    return render_template('index.html', characters=response['results'])