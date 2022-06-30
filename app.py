import json
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
env_var = os.environ.get('TEST_ENV_VAR')
app.secret_key = env_var

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys():
            flash('...Error...')
            return redirect(url_for('home'))

        urls[request.form['code']] = {'url': request.form['url']}
        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            flash('Your have successfully stord an url!!')
        return render_template('your_url.html', code=request.form['code'])
    return redirect(url_for('home'))
