from flask import Blueprint, request, jsonify
from app.utils.soap_client import get_soap_client
from config.config import Config

consulta_navio = Blueprint('consulta_navio', __name__)

@consulta_navio.route('/consulta_navio', methods=['GET'])
def consulta_navio_endpoint():
    data = request.json
    navio = data.get('Navio')
    status = data.get('Status')
    data_inicio = data.get('DataInicio')
    data_final = data.get('DataFinal')

    if not navio or not data_inicio or not data_final:
        return jsonify({"error": "Parâmetros 'Navio', 'DataInicio' e 'DataFinal' são obrigatórios!"}), 400

    client = get_soap_client(Config.WSDL_URL_NAVIO)
    try:
        response = client.service.ConsultaNavio(
            Navio=navio,
            Status=status,
            DataInicio=data_inicio,
            DataFinal=data_final
        )
        response_dict = response.__dict__ if hasattr(response, '__dict__') else str(response)
        return jsonify(response_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500