import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_style
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


def get_db_connection():
    url_db = os.getenv('DATABASE_URL')
    return psycopg2.connect(url_db)


@app.route('/')
def index():
    return render_template('index.html')
