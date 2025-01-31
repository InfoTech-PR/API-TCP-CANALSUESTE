from flask import Flask
from config.config import Config
import logging
from app.routes.consulta_navio import consulta_navio
from app.routes.agendamento_expo_cheio import agendar_unidade, consultar_grade, editar_agenda_unidade, deletar_agenda_unidade
from app.routes.expo_pre_stacking import obter_dados_booking, registrar_prestacking_cheio
from app.routes.expo_sol_embarque import consulta_due, solicitar_ordem_embarque_due, consulta_movimentacao
from app.routes.expo_rolagem import rolagem_carga, obter_dados_booking_rolagem
from app.routes.importacao import bloqueio_nvo, bloqueio_nvo_master, movimentacao_importacao

# logging.basicConfig(level=logging.DEBUG)

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
    app.register_blueprint(consulta_due)
    app.register_blueprint(solicitar_ordem_embarque_due)
    app.register_blueprint(consulta_movimentacao)
    # app.register_blueprint(rolagem_carga)
    # app.register_blueprint(obter_dados_booking_rolagem)
    app.register_blueprint(bloqueio_nvo)
    app.register_blueprint(bloqueio_nvo_master)
    app.register_blueprint(movimentacao_importacao)

    return app
