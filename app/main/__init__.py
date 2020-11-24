from flask import Flask

#from .config import config_by_name

#running on http://127.0.0.1:5000/
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    return app