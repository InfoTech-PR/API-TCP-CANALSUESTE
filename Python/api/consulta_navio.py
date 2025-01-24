from flask import Blueprint, request, jsonify
from zeep import Client
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
import requests
from config import Config

consulta_navio = Blueprint('consulta_navio', __name__)

@consulta_navio.route('/consulta_navio', methods=['GET'])
def consulta_navio_endpoint():
    # Obtendo os parâmetros diretamente da URL
    navio = request.args.get('Navio', default=None, type=str)
    status = request.args.get('Status', default=None, type=str)
    data_inicio = request.args.get('DataInicio', default=None, type=str)
    data_final = request.args.get('DataFinal', default=None, type=str)

    if not navio or not data_inicio or not data_final:
        return jsonify({"error": "Parametros 'Navio', 'DataInicio' e 'DataFinal' são obrigatórios!"}), 400

    # Configurações do SOAP e Autenticação
    auth = HTTPBasicAuth(Config.USERNAME, Config.PASSWORD)
    session = requests.Session()
    session.auth = auth

    # URL do serviço SOAP
    url = Config.WSDL_URL

    # Criando o cliente Zeep para consumir o serviço SOAP
    client = Client(url, transport=Transport(session=session))

    try:
        # Realizando a requisição ao serviço SOAP
        response = client.service.ConsultaNavio(
            Navio=navio,
            Status=status,
            DataInicio=data_inicio,
            DataFinal=data_final
        )

        # Retornando a resposta do serviço
        return jsonify(response)

    except Exception as e:
        # Retornando erro caso algo aconteça na consulta
        return jsonify({"error": str(e)}), 500
