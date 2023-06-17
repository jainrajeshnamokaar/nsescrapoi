from flask import Flask,render_template,jsonify,session
from .scraping_mode import Symbol,get_table_data_json_format
from os import urandom
from datetime import datetime
from os import listdir
from flask_caching import Cache


app = Flask(__name__);
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

app.config["SECRET_KEY"] = f"{urandom(100)}"  

from .view import views

app.register_blueprint(views,url_prefix='/')

