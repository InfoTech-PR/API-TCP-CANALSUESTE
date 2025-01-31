from flask import Blueprint, request, jsonify
from app.utils.soap_client import get_soap_client
from app.utils.soap_handler import call_soap_service
from config.config import Config

obter_dados_booking_rolagem = Blueprint('obter_dados_booking_rolagem', __name__)
rolagem_carga = Blueprint('rolagem_carga', __name__)

@obter_dados_booking_rolagem.route('/obter_dados_booking_rolagem', methods=['POST'])
def obter_dados_booking_rolagem_endpoint():
    data = request.json
    booking = data.get('Booking')
    armador = data.get('Armador')
    
    if not booking or not armador:
        return jsonify({"error": "Os parâmetros 'Booking' e 'Armador' são obrigatórios!"}), 400

    client = get_soap_client(Config.WSDL_URL_EMBARQUE)
    return call_soap_service(client, "DadosBookingRequest", Booking=booking, Armador=armador)

@rolagem_carga.route('/rolagem_carga', methods=['POST'])
def rolagem_carga_endpoint():
    data = request.json
    conteiner = data.get('Conteiner')
    booking = data.get('Booking')
    armador = data.get('Armador')
    navio_indefinido = data.get('NavioIndefinido', False)

    if not conteiner or not booking or not armador:
        return jsonify({"error": "Os parâmetros 'Conteiner', 'Booking' e 'Armador' são obrigatórios!"}), 400

    client = get_soap_client(Config.WSDL_URL_EMBARQUE)
    return call_soap_service(client, "RolagemCarga",Conteiner=conteiner, Booking=booking, Armador=armador, NavioIndefinido=navio_indefinido)