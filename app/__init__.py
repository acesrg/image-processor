import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property  # noqa: E402
from flask_restplus import Api  # noqa: E402
from flask import Blueprint  # noqa: E402

from .main.controller.normalized_indexes_controller import api as ndvi_api  # noqa: E402

werkzeug.cached_property = werkzeug.utils.cached_property

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK API',
          version='1.0',
          description=''
          )

api.add_namespace(ndvi_api, path='/images')
