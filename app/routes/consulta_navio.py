from flask import Blueprint, request, jsonify
from app.utils.soap_client import get_soap_client
from config.config import Config

consulta_navio = Blueprint('consulta_navio', __name__)

@consulta_navio.route('/consulta_navio', methods=['GET'])
def consulta_navio_endpoint():
    navio = request.args.get('Navio')
    status = request.args.get('Status')
    data_inicio = request.args.get('DataInicio')
    data_final = request.args.get('DataFinal')

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
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
