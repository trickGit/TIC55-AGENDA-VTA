
from main import app
from flask import jsonify

@app.route('/')
def home():
    return "Agenda VTA no Flask"

