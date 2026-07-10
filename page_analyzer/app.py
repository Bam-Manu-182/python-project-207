import os
import psycopg2
import validators
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

def get_database_connection():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

def truncate_text(text, limit=252):

    if not text:
        return ""

    string_text = " ".join(str(text).split()).strip()

    if len(string_text) > limit:
        return string_text[:limit] + "..."

    return string_text


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secreto')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def add_url():
    url_input = request.form.get('url')

    if not validators.url(url_input) or len(url_input) > 255:
        flash('URL no válido')
        return render_template('index.html'), 422

    parsed = urlparse(url_input)
    normalized_url = f"{parsed.scheme}://{parsed.netloc}".lower()

    conn = get_database_connection()
    repo = conn.cursor()

    repo.execute(
        "SELECT id FROM urls WHERE name = %s;",
        (normalized_url,)
    )
    existing = repo.fetchone()

    if existing:
        flash('La página ya existe')
        url_id = existing[0]
    else:
        repo.execute(
            "INSERT INTO urls (name, created_at) "
            "VALUES (%s, %s) RETURNING id;",
            (normalized_url, datetime.now())
        )
        url_id = repo.fetchone()[0]
        conn.commit()
        flash('La página se agregó correctamente')

    repo.close()
    conn.close()
    return redirect(url_for('show_url', id=url_id))


@app.route('/urls/<int:id>')
def show_url(id):
    conn = get_database_connection()
    repo = conn.cursor()

    repo.execute(
        "SELECT id, name, created_at FROM urls WHERE id = %s;",
        (id,)
    )
    url_raw = repo.fetchone()

    if not url_raw:
        repo.close()
        conn.close()
        return redirect(url_for('list_urls'))

    url = list(url_raw)
    url_name = str(url[1]).strip()

    if len(url_name) > 255:
        url[1] = truncate_text(url_name, limit=255)

    repo.execute(
        "SELECT id, url_id, status_code, h1, title, description, created_at "
        "FROM url_checks WHERE url_id = %s ORDER BY id DESC;",
        (id,)
    )
    checks_raw = repo.fetchall()

    checks = []
    for row in checks_raw:
        h1 = str(row[3]).strip() if row[3] else ''
        title = str(row[4]).strip() if row[4] else ''
        desc = str(row[5]).strip() if row[5] else ''

        #if len(h1) > 255:
        h1 = truncate_text(h1, limit=255)
        #if len(title) > 255:
        title = truncate_text(title, limit=255)
        #if len(desc) > 255:
        desc = truncate_text(desc, limit=255)

        checks.append((row[0], row[1], row[2], h1, title, desc, row[6]))

    repo.close()
    conn.close()
    return render_template('show.html', url=url, checks=checks)


@app.route('/urls')
def list_urls():
    conn = get_database_connection()
    repo = conn.cursor()

    repo.execute(
        "SELECT DISTINCT ON (urls.id) urls.id, urls.name, "
        "url_checks.created_at, url_checks.status_code "
        "FROM urls LEFT JOIN url_checks ON urls.id = url_checks.url_id "
        "ORDER BY urls.id DESC, url_checks.id DESC;"
    )
    urls = repo.fetchall()

    repo.close()
    conn.close()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def add_check(id):
    conn = get_database_connection()
    repo = conn.cursor()

    repo.execute("SELECT name FROM urls WHERE id = %s;", (id,))
    url_data = repo.fetchone()

    try:
        response = requests.get(url_data[0], timeout=5)
        response.raise_for_status()
        status_code = response.status_code

        soup = BeautifulSoup(response.text, 'html.parser')

        h1_tag = soup.find('h1')
        raw_h1 = h1_tag.text if h1_tag else ''

        title_tag = soup.find('title')
        raw_title = title_tag.text if title_tag else ''

        desc_tag = soup.find('meta', attrs={'name': 'description'})
        raw_desc = desc_tag.get('content', '') if desc_tag else ''

        h1 = truncate_text(raw_h1, limit=85)
        title = truncate_text(raw_title, limit=85)
        description = truncate_text(raw_desc, limit=85)


        repo.execute(
            "INSERT INTO url_checks "
            "(url_id, status_code, h1, title, description, created_at) "
            "VALUES (%s, %s, %s, %s, %s, %s);",
            (id, status_code, h1, title, description, datetime.now())
        )
        conn.commit()
        flash('La página fue verificada correctamente')

    except requests.RequestException:
        flash('Ocurrió un error durante la verificación')

    repo.close()
    conn.close()
    return redirect(url_for('show_url', id=id))
