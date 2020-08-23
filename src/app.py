from flask import Flask, request, render_template, url_for
from markupsafe import escape
from generateLocations import getPOIList
num=1
# from flask_cors import CORS as cors

app = Flask(__name__, static_folder='static')

@app.route('/') # localhost:5000/
def returnIndex2():
    return render_template('index.html')

@app.route('/index/')
def returnIndex():
    return render_template('index.html')

@app.route('/howToUse/')
def returnHow():
    return render_template('howToUse.html')

@app.route('/tracker/')
def returnTracker():
    return render_template('tracker.html')




if __name__=="__main__":
    app.run(debug=True) # for local use only. see deployment flask for hosting