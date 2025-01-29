from flask import Blueprint, request, jsonify
from app.utils.soap_client import get_soap_client
from config.config import Config

obter_dados_booking = Blueprint('obter_dados_booking', __name__)
registrar_prestacking_cheio = Blueprint('registrar_prestacking_cheio', __name__)

@obter_dados_booking.route('/obter_dados_booking', methods=['GET'])
def obter_dados_booking_endpoint():
    

@registrar_prestacking_cheio.route('/registrar_prestacking_cheio', methods=['POST'])
def registrar_prestacking_cheio_endpoint():