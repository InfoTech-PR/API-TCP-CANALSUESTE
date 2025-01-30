from flask import Blueprint, request, jsonify
from app.utils.soap_client import get_soap_client
from config.config import Config

consulta_due = Blueprint('consulta_due', __name__)
solicitar_ordem_embarque_due = Blueprint('solicitar_ordem_embarque_due', __name__)

@consulta_due.route('/consulta_due', methods=['GET'])
def consulta_due_booking_endpoint():
    data = request.json
    numero_due = data.get('NumeroDue')
    if not numero_due:
        return jsonify({"error": "Parâmetro 'NumeroDue' é obrigatório!"}), 400

    client = get_soap_client(Config.WSDL_URL_EMBARQUE)
    try:
        response = client.service.ConsultarDue(NumeroDue=numero_due)
        response_dict = to_serializable(response)
        return jsonify(response_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500 

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
    try:
        response = client.service.SolicitarOrdemEmbarqueDue(NumeroDue=numero_due, AceiteAvarias=aceite_avarias, Conteineres=conteineres_soap)
        response_dict = to_serializable(response)
        return jsonify(response_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500