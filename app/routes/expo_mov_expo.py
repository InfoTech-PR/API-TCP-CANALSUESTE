from flask import Blueprint, request, jsonify
from app.utils.soap_client import get_soap_client
from app.utils.soap_handler import call_soap_service
from config.config import Config

consulta_movimentacao = Blueprint('consulta_movimentacao', __name__)

@consulta_movimentacao.route('/consulta_movimentacao', methods=['GET'])
def consulta_movimentacao_endpoint():
    data = request.json
    data_inicio = data.get('DataInicio')
    data_fim = data.get('DataFim')

    if not data_inicio or not data_fim:
        return jsonify({"error": "Parâmetros 'DataInicio', 'DataFim' são obrigatórios!"}), 400

    client = get_soap_client(Config.WSDL_URL_EMBARQUE)
    return call_soap_service(client, "ConsultarMovimentacao", DataInicio=data_inicio, DataFim=data_fim)