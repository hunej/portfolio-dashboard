# main.py

import json
from flask import Flask, render_template
from src.bubble_data import get_bubble_data

app = Flask(__name__)

@app.route('/')
def index():
    bubble_data = get_bubble_data()
    return render_template('index.html', bubble_data=bubble_data)

if __name__ == '__main__':
    app.run(debug=True)