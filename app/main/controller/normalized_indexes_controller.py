import flask
from flask import request
from flask_restplus import Resource
from ..service import normalized_indexes


class NdviApi:
    api = Namespace('ndvi', description='')


api = NdviApi.api


@api.route('/ndvi')
class CalculateNDVI(Resource):
    @api.response(200, 'NDVI successfully calculated and stored.')
    @api.doc('calculate ndvi')
    def post(self):
        """
        calculate ndvi
        """
        json_data = request.json
        image_path = json_data["image_path"]  # validar que el path sea válido
        # validar que el path tenga adentro imágenes?
        information = normalized_indexes.InitInformation(image_path)  # validar la creación de la instancia
        return flask.jsonify(information._init_satellite_image())   # validar que la respuesta sea un json válido (con los atributos que corresponde)
