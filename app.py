import json
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from werkzeug.utils import secure_filename


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

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        elif 'file' in request.files.keys():
            if 'file' not in request.files: 
                flash('No file found...')
            file = request.files.get('file')

            if file.filename == '':
                flash('No selected file')
                return redirect('home')

            full_name = request.form['code'] + file.filename

            if file and full_name: 
                file_name = secure_filename(full_name)
                file.save('/Users/samsan/Desktop/Coding/Flask Training/Flask/images/' + file_name)

        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            flash('Your have successfully stord an url!!')
        return render_template('your_url.html', code=request.form['code'])
    return redirect(url_for('home'))

@app.route('/<string:code>')
def url_redirect(code): 
    if os.path.exists('urls.json'):
        with open('urls.json') as json_file:
            deserialized = json.load(json_file)
            if code in deserialized.keys():
                if 'url' in deserialized[code].keys():
                    return redirect(deserialized[code]['url'])
            flash('Not found')
            return redirect(url_for('home'))
