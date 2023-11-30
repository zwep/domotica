from flask import Flask, render_template

# import config
import re
import os

app = Flask(__name__)

@app.route('/plot')
def plot():
    return render_template('plot.html')

@app.route('/')
def index():
    return render_template('index.html')
