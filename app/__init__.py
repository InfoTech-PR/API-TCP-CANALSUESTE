from flask import Flask
from config.config import Config
from app.routes.consulta_navio import consulta_navio
from app.routes.agendamento_expo_cheio import agendar_unidade, consultar_grade, editar_agenda_unidade, deletar_agenda_unidade
from app.routes.expo_pre_stacking import registrar_prestacking_cheio, obter_dados_booking

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(consulta_navio)
    app.register_blueprint(consultar_grade)
    app.register_blueprint(agendar_unidade)
    app.register_blueprint(editar_agenda_unidade)
    app.register_blueprint(deletar_agenda_unidade)
    app.register_blueprint(registrar_prestacking_cheio)
    app.register_blueprint(obter_dados_booking)

    return app
