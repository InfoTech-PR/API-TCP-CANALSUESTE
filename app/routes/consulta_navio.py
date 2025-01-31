from flask import Blueprint, request, jsonify
from app.utils.soap_client import get_soap_client
from config.config import Config
from app.utils.soap_handler import call_soap_service

consulta_navio = Blueprint('consulta_navio', __name__)

@consulta_navio.route('/consulta_navio', methods=['POST'])
def consulta_navio_endpoint():
    data = request.json
    navio = data.get('Navio')
    status = data.get('Status')
    data_inicio = data.get('DataInicio')
    data_final = data.get('DataFinal')

    if not data_inicio or not data_final:
        return jsonify({"error": "Parâmetros 'DataInicio' e 'DataFinal' são obrigatórios!"}), 400

    client = get_soap_client(Config.WSDL_URL_NAVIO)
    
    return call_soap_service(client, "ConsultaNavio", Navio=navio, Status=status, DataInicio=data_inicio, DataFinal=data_final)
