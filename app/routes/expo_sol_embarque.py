from flask import Blueprint, request, jsonify
from app.utils.soap_client import get_soap_client
from app.utils.soap_handler import call_soap_service
from config.config import Config

consulta_due = Blueprint('consulta_due', __name__)
solicitar_ordem_embarque_due = Blueprint('solicitar_ordem_embarque_due', __name__)
consulta_movimentacao = Blueprint('consulta_movimentacao', __name__)
consulta_booking = Blueprint('consulta_booking', __name__)
excluir_conteiner = Blueprint('excluir_conteiner', __name__)
rolagem_carga = Blueprint('rolagem_carga', __name__)

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

@consulta_booking.route('/consulta_booking', methods=['POST'])
def consulta_booking_endpoint():
    data = request.json
    booking = data.get('Booking')
    armador = data.get('Armador')
    
    if not booking or not armador:
        return jsonify({"error": "Os parâmetros 'Booking' e 'Armador' são obrigatórios!"}), 400

    client = get_soap_client(Config.WSDL_URL_EMBARQUE)
    return call_soap_service(client, "ConsultaBooking", Booking=booking, Armador=armador)

@excluir_conteiner.route('/excluir_conteiner', methods=['POST'])
def excluir_conteiner_endpoint():
    data = request.json
    conteiner = data.get('Conteiner')

    if not conteiner:
        return jsonify({"error": "O parâmetro 'Conteiner' é obrigatórios!"}), 400

    client = get_soap_client(Config.WSDL_URL_EMBARQUE)
    return call_soap_service(client, "ExclusaoConteiner", ExclusaoConteiner={"Conteiner": conteiner})

@rolagem_carga.route('/rolagem_carga', methods=['POST'])
def rolagem_carga_endpoint():
    data = request.json
    conteiner = data.get('Conteiner')
    booking = data.get('Booking')
    armador = data.get('Armador')
    navio_indefinido = data.get('NavioIndefinido', False)

    if not conteiner or not booking or not armador or not navio_indefinido:
        return jsonify({"error": "Os parâmetros 'Conteiner', 'Booking', 'Armador' e 'NavioIndefinido' são obrigatórios!"}), 400

    client = get_soap_client(Config.WSDL_URL_EMBARQUE)
    return call_soap_service(client, "RolagemCarga",Conteiner=conteiner, Booking=booking, Armador=armador, NavioIndefinido=navio_indefinido)