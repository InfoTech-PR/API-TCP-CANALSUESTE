from flask import Blueprint, request, jsonify
from zeep import Client
from requests.auth import HTTPBasicAuth
import requests

consulta_navio = Blueprint('consulta_navio', __name__)

@consulta_navio.route('/consulta_navio', methods=['GET'])
def consulta_navio_endpoint():
    navio = request.args.get('Navio', default="MSC MELINE", type=str)
    status = request.args.get('Status', default="", type=str)
    data_inicio = request.args.get('DataInicio', default="2019-05-24", type=str)
    data_final = request.args.get('DataFinal', default="2019-05-24", type=str)

    # URL do serviço SOAP
    url = 'https://wsc-hom.tcp.com.br/services/WebservicesClientes_ConsultaPublica?wsdl'

    # Autenticação (usuário e senha)
    auth = HTTPBasicAuth('wssueste', '!wssueste&2024%')
    session = requests.Session()
    session.auth = auth

    # Configurando o cliente Zeep
    client = Client(url, transport=Transport(session=session))

    # Fazendo a requisição SOAP
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
