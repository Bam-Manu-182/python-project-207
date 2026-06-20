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

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secreto')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def add_url():
    url_input = request.form.get('url')

    if not validators.url(url_input) or len(url_input) > 255:
        flash('URL incorrecta')
        return redirect(url_for('index'))

    parsed = urlparse(url_input)
    normalized_url = f"{parsed.scheme}://{parsed.netloc}"

    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
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
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    repo = conn.cursor()

    repo.execute(
        "SELECT id, name, created_at FROM urls WHERE id = %s;",
        (id,)
    )
    url = repo.fetchone()

    repo.execute(
        "SELECT id, url_id, status_code, h1, title, description, created_at "
        "FROM url_checks WHERE url_id = %s ORDER BY id DESC;",
        (id,)
    )
    checks_raw = repo.fetchall()

    checks = []
    for row in checks_raw:
        h1 = row[3] if row[3] else ''
        title = row[4] if row[4] else ''
        desc = row[5] if row[5] else ''

        checks.append((row[0], row[1], row[2], h1, title, desc, row[6]))

    repo.close()
    conn.close()
    return render_template('show.html', url=url, checks=checks)


@app.route('/urls')
def list_urls():
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
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
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    repo = conn.cursor()

    repo.execute("SELECT name FROM urls WHERE id = %s;", (id,))
    url_data = repo.fetchone()

    try:
        response = requests.get(url_data[0], timeout=5)
        response.raise_for_status()
        status_code = response.status_code

        soup = BeautifulSoup(response.text, 'html.parser')

        h1_tag = soup.find('h1')
        h1 = str(h1_tag.text).strip() if h1_tag else ''
        if len(h1) > 255:
            h1 = h1[:252] + '...'

        title_tag = soup.find('title')
        title = str(title_tag.text).strip() if title_tag else ''
        if len(title) > 255:
            title = title[:252] + '...'

        desc_tag = soup.find('meta', attrs={'name': 'description'})
        description = desc_tag.get('content', '') if desc_tag else ''
        description = str(description).strip()
        if len(description) > 255:
            description = description[:252] + '...'

        repo.execute(
            "INSERT INTO url_checks "
            "(url_id, status_code, h1, title, description, created_at) "
            "VALUES (%s, %s, %s, %s, %s, %s);",
            (id, status_code, h1, title, description, datetime.now())
        )
        conn.commit()
        flash('La página fue verificada correctamente')

    except requests.RequestException:
        flash('Ocurrió un error al hacer la verificación.')

    repo.close()
    conn.close()
    return redirect(url_for('show_url', id=id))
