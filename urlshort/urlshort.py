import json
from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
from werkzeug.utils import secure_filename
from datetime import datetime
import os
# from dotenv import load_dotenv
# bp = Flask(__name__)


# load_dotenv()
# env_var = os.environ.get('TEST_ENV_VAR')
# app.secret_key = env_var

bp = Blueprint('urlshort', __name__, template_folder='templates')

@bp.route('/')
def home():
    return render_template('home.html',codes=session.keys())


@bp.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}
        
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys():
            flash('...Error...')
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        elif 'file' in request.files.keys():
            if 'file' not in request.files:
                flash('No file found...')

            file = request.files.get('file')

            if file.filename == '':
                flash('No selected file')
                return redirect(url_for('urlshort.home'))

            full_name = request.form['code'] + secure_filename(file.filename)

            if file and full_name:
                file.save(
                    '/Users/samsan/Desktop/Coding/Flask Training/Flask/urlshort/static/user_files/' + full_name)
                urls[request.form['code']] = {'file': full_name}

        with open('urls.json', 'w') as url_file:
            deserialized = json.dump(urls, url_file)
            session[request.form['code']] = True
            flash('Your have successfully stord an url!!')
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('urlshort.home'))


@bp.route('/<string:code>')
def url_redirect(code):
    if os.path.exists('urls.json'):

        with open('urls.json') as json_file:
            deserialized = json.load(json_file)

            if code in deserialized.keys():
                if 'url' in deserialized[code].keys():
                    return redirect(deserialized[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + deserialized[code]['file']))
    return abort(404)


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))