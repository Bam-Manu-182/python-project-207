import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from psycopg2 import connect
from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret_key_por_defecto')


def get_db_connection():
    database_url = os.getenv('DATABASE_URL')
    return connect(database_url)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET'])
def get_urls():
    conn = get_db_connection()
    with conn.cursor(cursor_factory=NamedTupleCursor) as curr:
        curr.execute('''
            SELECT DISTINCT ON (urls.id)
                urls.id,
                urls.name,
                url_checks.created_at as last_check,
                url_checks.status_code
            FROM urls
            LEFT JOIN url_checks ON urls.id = url_checks.url_id
            ORDER BY urls.id DESC, url_checks.id DESC;
        ''')
        urls_data = curr.fetchall()
    conn.close()
    return render_template('urls/index.html', urls=urls_data)


@app.route('/urls', methods=['POST'])
def post_url():
    url_form = request.form.get('url')

    if not url_form:
        flash('URL incorrecta', 'danger')
        return render_template('index.html'), 422

    conn = get_db_connection()
    with conn.cursor(cursor_factory=NamedTupleCursor) as curr:
        curr.execute('SELECT id FROM urls WHERE name = %s;', (url_form,))
        existing_url = curr.fetchone()

        if existing_url:
            flash('La página ya existe', 'info')
            conn.close()
            return redirect(url_for('get_url_detail', id=existing_url.id))

        curr.execute(
            'INSERT INTO urls (name) VALUES (%s) RETURNING id;',
            (url_form,)
        )
        new_id = curr.fetchone().id
        conn.commit()
    conn.close()

    flash('Página añadida con éxito', 'success')
    return redirect(url_for('get_url_detail', id=new_id))


@app.route('/urls/<int:id>', methods=['GET'])
def get_url_detail(id):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=NamedTupleCursor) as curr:
        curr.execute('SELECT * FROM urls WHERE id = %s;', (id,))
        url_data = curr.fetchone()

        if not url_data:
            conn.close()
            return "Página no encontrada", 404

        curr.execute(
            'SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC;',
            (id,)
        )
        checks = curr.fetchall()
    conn.close()

    return render_template('urls/show.html', url=url_data, checks=checks)


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id):
    conn = get_db_connection()
    url_data = None

    with conn.cursor(cursor_factory=NamedTupleCursor) as curr:
        curr.execute('SELECT name FROM urls WHERE id = %s;', (id,))
        url_data = curr.fetchone()

    if not url_data:
        conn.close()
        flash('Ocurrió un error al hacer la verificación.', 'danger')
        return redirect(url_for('get_urls'))

    try:
        response = requests.get(url_data.name, timeout=5)
        response.raise_for_status()
        status_code = response.status_code

        with conn.cursor(cursor_factory=NamedTupleCursor) as curr:
            curr.execute(
                'INSERT INTO url_checks (url_id, status_code) VALUES (%s, %s);',
                (id, status_code)
            )
            conn.commit()

        flash('Página verificada con éxito', 'success')

    except requests.RequestException:
        flash('Ocurrió un error al hacer la verificación.', 'danger')

    finally:
        conn.close()

    return redirect(url_for('get_url_detail', id=id))


if __name__ == '__main__':
    app.run()
