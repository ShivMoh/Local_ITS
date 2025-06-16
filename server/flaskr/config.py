import os
from flask import Flask
from flask_cors import CORS
from flaskr import db
from flaskr.api import inference, auth, test, file

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    print("path", app.instance_path)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    app.register_blueprint(inference.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(test.bp)
    app.register_blueprint(file.bp)

    app.config.from_prefixed_env()

    return app





