from flask import Flask, render_template
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret_key_default')

@app.route('/')
def index():
    return render_template('index.html', title='Hello, Flask!')

if __name__ == '__main__':
    app.run()
