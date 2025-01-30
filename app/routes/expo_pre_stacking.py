from flask import Blueprint, request, jsonify
from app.utils.soap_client import get_soap_client
from config.config import Config

obter_dados_booking = Blueprint('obter_dados_booking', __name__)
registrar_prestacking_cheio = Blueprint('registrar_prestacking_cheio', __name__)

@obter_dados_booking.route('/obter_dados_booking', methods=['GET'])
def obter_dados_booking_endpoint():
    data = request.json
    booking = data.get('Booking')
    armador = data.get('Armador')
    if not booking or not armador:
        return jsonify({"error": "Parâmetro 'Armador' e 'Booking' é obrigatório!"}), 400

    client = get_soap_client(Config.WSDL_URL_PRESTACKING)
    try:
        response = client.service.ObterDadosBooking(Booking=booking, Armador=armador)
        response_dict = to_serializable(response)
        return jsonify(response_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500  

@registrar_prestacking_cheio.route('/registrar_prestacking_cheio', methods=['POST'])
def registrar_prestacking_cheio_endpoint():
    data = request.json
    
    lista_nfe = data.get('ListaNFe')
    dados_exportacao = data.get('DadosExportacao')

    if not lista_nfe or not dados_exportacao:
        return jsonify({"error": "Os campos 'ListaNFe' e 'DadosExportacao' são obrigatórios!"}), 400
    
    prestacking_request = {
        'ListaNFe': lista_nfe,
        'DadosExportacao': dados_exportacao  
    }
    client = get_soap_client(Config.WSDL_URL_PRESTACKING)
    
    try:
        response = client.service.RegistrarPrestackingCheio(
            ListaNFe=lista_nfe, 
            DadosExportacao=dados_exportacao 
        )
        response_dict = to_serializable(response)
        return jsonify(response_dict)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
