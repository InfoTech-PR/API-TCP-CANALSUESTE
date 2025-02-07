from flask import Blueprint, Response, request, jsonify
from app.utils.soap_client import get_soap_client
from app.utils.soap_handler import call_soap_service
from app.utils.validators import testar_conexao
from config.config import Config
from sqlalchemy import text

obter_dados_booking = Blueprint('obter_dados_booking', __name__)
registrar_prestacking_cheio = Blueprint('registrar_prestacking_cheio', __name__)

engine = testar_conexao(Config.DATABASE_URI)

@obter_dados_booking.route('/obter_dados_booking', methods=['POST'])
def obter_dados_booking_endpoint():
    try:
        data = request.get_json()
        codigo = data.get('CODIGO')

        if not codigo:
            return jsonify({"error": "Parâmetro 'CODIGO' é obrigatório!"}), 400

        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT CODIGO
                FROM controle_processos
                WHERE CODIGO = :codigo
            """), {'codigo': codigo})
            controle_processos = result.fetchone()

        if not controle_processos:
            return jsonify({"error": f"Nenhum controle encontrado para o CODIGO {codigo}."}), 404

        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT BOOKING, ARMADOR, CONTAINER 
                FROM containers_processos 
                WHERE flag = 'S' AND COD_CONTROLE_PROCESSO = :codigo
            """), {'codigo': codigo})
            conteiners = [dict(row) for row in result.mappings()]

        if not conteiners:
            return jsonify({"error": "Nenhum contêiner com flag 'S' encontrado."}), 404

        client = get_soap_client(Config.WSDL_URL_PRESTACKING)
        response_data = []

        for c in conteiners:
            container_id = c["CONTAINER"]
            booking = c["BOOKING"]
            armador = c["ARMADOR"]

            if not booking or not armador:
                response_data.append({
                    "container": container_id,
                    "error": "Parâmetro 'Armador' e 'Booking' é obrigatório!"
                })
                continue
            try:
                response = call_soap_service(client, "ObterDadosBooking", Booking=booking, Armador=armador)

                if isinstance(response, Response):  
                    soap_response = response.get_json() 
                else:
                    soap_response = response 

                response_data.append({
                    "container": container_id,
                    "booking": booking,
                    "armador": armador,
                    "response": soap_response
                })
            except Exception as e:
                response_data.append({
                    "container": container_id,
                    "booking": booking,
                    "armador": armador,
                    "error": str(e)
                })
        return jsonify(response_data), 200

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
    return call_soap_service(client, "RegistrarPrestackingCheio", ListaNFe=lista_nfe, DadosExportacao=dados_exportacao)