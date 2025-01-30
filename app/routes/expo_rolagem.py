from flask import Blueprint, request, jsonify
from app.utils.soap_client import get_soap_client
from config.config import Config

# obter_dados_booking = Blueprint('obter_dados_booking', __name__)
rolagem_carga = Blueprint('rolagem_carga', __name__)

# @obter_dados_booking.route('/obter_dados_booking', methods=['POST'])
# def obter_dados_booking_endpoint():
    # data = request.json
    # booking = data.get('Booking')
    # armador = data.get('Armador')
    
    # if not booking or not armador:
    #     return jsonify({"error": "Os parâmetros 'Booking' e 'Armador' são obrigatórios!"}), 400

    # client = get_soap_client(Config.WSDL_URL_EMBARQUE)
    # try:
    #     response = client.service.DadosBookingRequest(Booking=booking, Armador=armador)
    #     response_dict = to_serializable(response)
    #     return jsonify(response_dict)
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500

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
    try:
        response = client.service.RolagemCarga(
            Conteiner=conteiner,
            Booking=booking,
            Armador=armador,
            NavioIndefinido=navio_indefinido
        )
        response_dict = to_serializable(response)
        return jsonify(response_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
