from flask import Blueprint, request, jsonify
from app.utils.soap_client import get_soap_client
from app.utils.validators import validar_parametros_obrigatorios
from app.utils.soap_handler import call_soap_service
from config.config import Config

consulta_navio = Blueprint('consulta_navio', __name__)

@consulta_navio.route('/consulta_navio', methods=['POST'])
def consulta_navio_endpoint():
    data = request.json
    parametros_obrigatorios = ["DataInicio", "DataFinal"]
        
    navio = data.get('Navio')
    status = data.get('Status')
    data_inicio = data.get('DataInicio')
    data_final = data.get('DataFinal')

    erro = validar_parametros_obrigatorios(data, parametros_obrigatorios)
    if erro:
        return erro
    client = get_soap_client(Config.WSDL_URL_NAVIO)
    
    return call_soap_service(client, "ConsultaNavio", Navio=navio, Status=status, DataInicio=data_inicio, DataFinal=data_final)
