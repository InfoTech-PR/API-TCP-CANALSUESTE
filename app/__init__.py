from flask import Flask
from config.config import Config
from app.routes.consulta_navio import consulta_navio
from app.routes.consulta_grade import consulta_grade

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(consulta_navio)
    app.register_blueprint(consulta_grade)

    return app
