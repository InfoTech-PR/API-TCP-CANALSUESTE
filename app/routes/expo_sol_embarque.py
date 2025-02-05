from flask import Blueprint, request, jsonify
from app.utils.soap_client import get_soap_client
from app.utils.soap_handler import call_soap_service
from config.config import Config

consulta_due = Blueprint('consulta_due', __name__)
solicitar_ordem_embarque_due = Blueprint('solicitar_ordem_embarque_due', __name__)
consulta_movimentacao = Blueprint('consulta_movimentacao', __name__)

@consulta_movimentacao.route('/consulta_movimentacao', methods=['POST'])
def consulta_movimentacao_endpoint():
    data = request.json
    data_inicio = data.get('DataInicio')
    data_fim = data.get('DataFim')
    empresa = data.get('EmpresaSelecionada')

    if not data_inicio or not data_fim:
        return jsonify({"error": "Parâmetros 'DataInicio' e 'DataFim' são obrigatórios!"}), 400

    client = get_soap_client(Config.WSDL_URL_EMBARQUE, empresa=empresa)
    return call_soap_service(client, "ConsultarMovimentacao", DataInicio=data_inicio, DataFim=data_fim)

@consulta_due.route('/consulta_due', methods=['POST'])
def consulta_due_booking_endpoint():
    data = request.json
    numero_due = data.get('NumeroDue')
    if not numero_due:
        return jsonify({"error": "Parâmetro 'NumeroDue' é obrigatório!"}), 400

    client = get_soap_client(Config.WSDL_URL_EMBARQUE)
    return call_soap_service(client, "ConsultarDue", NumeroDue=numero_due)

@solicitar_ordem_embarque_due.route('/solicitar_ordem_embarque_due', methods=['POST'])
def solicitar_ordem_embarque_due_endpoint():
    data = request.json
    numero_due = data.get('NumeroDue')
    aceite_avarias = data.get('AceiteAvarias')
    conteineres = data.get('Conteineres', [])

    if not numero_due or aceite_avarias is None or not conteineres:
        return jsonify({"error": "Parâmetro  'NumeroDue', 'AceiteAvarias' e 'Conteineres' é obrigatório!"}), 400

    if not isinstance(conteineres, list):
        return jsonify({"error": "'Conteineres' deve ser uma lista de contêineres!"}), 400

    conteineres_soap = [{"Conteiner": c["Conteiner"]} for c in conteineres]
    client = get_soap_client(Config.WSDL_URL_EMBARQUE)
    return call_soap_service(client, "SolicitarOrdemEmbarqueDue", NumeroDue=numero_due, AceiteAvarias=aceite_avarias, Conteineres=conteineres_soap)