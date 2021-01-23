import werkzeug
from flask_restplus import Api
from flask import Blueprint
from .main.controller.normalized_indexes_controller import api as ndvi_api

werkzeug.cached_property = werkzeug.utils.cached_property

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK API',
          version='1.0',
          description=''
          )

api.add_namespace(ndvi_api, path='/images')
