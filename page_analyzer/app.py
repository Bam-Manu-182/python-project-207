from flask import Flask, render_template, request, redirect, url_for, flash
import os
import psycopg2
from psycopg2.extras import NamedTupleCursor
from urllib.parse import urlparse
import validators
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret_key_default')
DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def add_url():
    url_input = request.form.get('url')

    if not validators.url(url_input) or len(url_input) > 255:
        flash('URL incorrecta', 'danger')
        return render_template('index.html'), 422

    parsed_url = urlparse(url_input)
    normalized_name = f"{parsed_url.scheme}://{parsed_url.netloc}"

    conn = get_db_connection()
    with conn.cursor(cursor_factory=NamedTupleCursor) as curr:
        curr.execute('SELECT id FROM urls WHERE name = %s;', (normalized_name,))
        existing_url = curr.fetchone()

        if existing_url:
            flash('La página ya existe', 'info')
            url_id = existing_url.id
        else:
            curr.execute(
                'INSERT INTO urls (name) VALUES (%s) RETURNING id;',
                (normalized_name,)
            )
            url_id = curr.fetchone().id
            conn.commit()
            flash('Página añadida con éxito', 'success')

    conn.close()

    return redirect(url_for('get_url_detail', id=url_id))


@app.route('/urls/<int:id>')
def get_url_detail(id):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=NamedTupleCursor) as curr:
        curr.execute('SELECT * FROM urls WHERE id = %s;', (id,))
        url_data = curr.fetchone()
    conn.close()

    if not url_data:
        return "Página no encontrada", 404

    return render_template('urls/show.html', url=url_data)


@app.route('/urls')
def get_urls():
    conn = get_db_connection()
    with conn.cursor(cursor_factory=NamedTupleCursor) as curr:
        curr.execute('SELECT * FROM urls ORDER BY id DESC;')
        urls = curr.fetchall()
    conn.close()
    return render_template('urls/index.html', urls=urls)


if __name__ == '__main__':
    app.run()
