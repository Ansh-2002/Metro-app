from flask import *
import sys, os
import urllib.request, json
from jinja2 import Template
import json

app = Flask(__name__)

@app.route("/", methods =["GET", "POST"])
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/helpline")
def help():
    return render_template('helpline.html')

@app.route("/teams")
def team():
    return render_template('teams.html')

@app.route("/path")
def route():
    source = request.args.get("from", "Dwarka").replace(' ','%20')
    destination = request.args.get("to", "Palam").replace(' ','%20')
    url="https://us-central1-delhimetroapi.cloudfunctions.net/route-get?from=" + source + "&to=" + destination
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    if dict['status'] != 200:
        status = dict['status']
        msg=" 404 not found"
        if status == 204:
            msg="same source and destination"
        elif status == 4061:
            msg="Invalid Source"
        elif status == 4062:
            msg="Invalid Destination"
        elif status == 406:
            msg = "Invalid Source and Destination"
        return render_template ("faliure.html",status=msg)
    else:
        syle = "border-color: " + dict['line1'][0] + ";"
        cost = 0
        n=len(dict['path'])
        if n<=3:
            cost=10
        if n<=9:
            cost=20
        if n<=16:
            cost= 30
        if n<=25:
            cost=40
        if n<=35:
            cost=50
        else:
            cost =60
        return render_template ("path.html", syle=syle,dict=dict,cost=cost)

@app.route("/map")
def map():
    return render_template('map.html')

@app.route("/test")
def test():
    return render_template('test.html')
app.run()

@app.route("/nearest")
def nearest():
    return render_template('nearest.html')

@app.route("/search")
def search():
    searchName = request.args.get("search", "Dwarka")
    return render_template('search.html',searchName=searchName)

@app.route('/<path:catch_all>')
def catch_all(catch_all):
    return redirect('/')
if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')
