from urlshort import urlshort
from flask import Flask
import os


def create_app(test_config=None):

    app = Flask(__name__)

    env_var = os.environ.get('TEST_ENV_VAR')
    app.secret_key = env_var

    app.register_blueprint(urlshort.bp)

    return app
