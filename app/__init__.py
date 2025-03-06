from flask import Flask, Response
from flasgger import Swagger
from config.config import Config
from datetime import datetime
from flask_cors import CORS
from collections import OrderedDict
from app.routes.consulta_navio import consulta_navio
from app.routes.agendamento_expo_cheio import agendar_unidade, consultar_grade, editar_agenda_unidade, deletar_agenda_unidade
from app.routes.expo_pre_stacking import obter_dados_booking, registrar_prestacking_cheio
from app.routes.expo_sol_embarque import consulta_due, solicitar_ordem_embarque_due, consulta_movimentacao, consulta_booking, excluir_conteiner, rolagem_carga
from app.routes.importacao import bloqueio_nvo, bloqueio_nvo_master, movimentacao_importacao
import json

start_time = datetime.now()

def get_uptime():
    uptime = datetime.now() - start_time
    return f"{uptime.seconds // 3600}h {uptime.seconds % 3600 // 60}m {uptime.seconds % 60}s"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    Swagger(app)
    
    @app.route('/', methods=['GET'])
    def home():
        response = OrderedDict({
            "status": "API-TCP-CANALSUESTE",
            "uptime": get_uptime(),
            "timestamp": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            "developed": "Josue Henrique",
            "portfolio": "https://josuashenrique.site/",
            "rotas": [
                "GET /",
                "GET /consulta-navio",
                "POST /agendar-unidade",
                "GET /consultar-grade",
                "PATCH /editar-agenda-unidade",
                "DELETE /deletar-agenda-unidade",
                "GET /obter-dados-booking",
                "GET /registrar-prestacking-cheio",
                "GET /consulta-due",
                "POST /solicitar-ordem-embarque-due",
                "GET /consulta-movimentacao",
                "GET /consulta-booking",
                "DELETE /excluir-conteiner",
                "POST /rolagem-carga",
                "POST /bloqueio-nvo",
                "POST /bloqueio-nvo-master",
                "GET /movimentacao-importacao"
            ]
        })
        return Response(json.dumps(response, ensure_ascii=False, indent=4, sort_keys=False), mimetype="application/json")

    # Registrar rotas
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
    app.register_blueprint(rolagem_carga)
    app.register_blueprint(excluir_conteiner)
    app.register_blueprint(consulta_booking)
    app.register_blueprint(bloqueio_nvo)
    app.register_blueprint(bloqueio_nvo_master)
    app.register_blueprint(movimentacao_importacao)

    return app
