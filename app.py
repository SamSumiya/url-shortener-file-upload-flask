from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def home(): 
    return render_template('home.html')

@app.route('/your-url')
def your_url():
    print(request.args['code'], 'this is a request')
    return render_template('your_url.html', code=request.args['code'])
