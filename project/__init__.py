from flask import Flask, jsonify
from flask_cors import CORS
# from flaskext.mysql import MySQL

from project.apis import api
from project.config import load_config_test, load_all_configs
from project.core.Connect import CoreConnect

from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint


import threading
import json


def create_app(is_test):
    # Create flask app
    app = Flask(__name__)







    with app.app_context():

        SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')

        @app.route("/docs/swagger.json")
        def spec():
            swag = swagger(app)
            swag['info']['version'] = "1.0"
            swag['info']['title'] = "Test API Mon Ami Poto"
            return jsonify(swag)

        # Call factory function to create our blueprint
        swaggerui_blueprint = get_swaggerui_blueprint(
            SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
            "/docs/swagger.json",
            config={  # Swagger UI config overrides
                'app_name': "Test API Mon Ami Poto"
            },
            # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
            #    'clientId': "your-client-id",
            #    'clientSecret': "your-client-secret-if-required",
            #    'realm': "your-realms",
            #    'appName': "your-app-name",
            #    'scopeSeparator': " ",
            #    'additionalQueryStringParams': {'test': "hello"}
            # }
        )

        app.register_blueprint(swaggerui_blueprint)

        if is_test:
            load_config_test(app)
        else:
            load_all_configs(app)
        # Init api
        api.init_app(app)
        # Init CORS
        CORS(app, origins=['.*monamipoto.com', '.*localhost.*', '*localhost*'])

    return app
