from flask import Flask, request, render_template
from markupsafe import escape
# from flask_cors import CORS as cors

app = Flask(__name__)

@app.route('/') # localhost:5000/
def getdata():
    geocode = 12.35
    asdf  =   "hello there"
    return render_template('tester.html', owovar=geocode, asdf=asdf)

@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(escape(username))




if __name__=="main":
    app.run(debug=True) # for local use only. see deployment flask for hosting