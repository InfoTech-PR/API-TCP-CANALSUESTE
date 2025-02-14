from flask import Blueprint, Response, json, request, jsonify
from app.utils.soap_client import get_soap_client
from app.utils.soap_handler import call_soap_service
from app.utils.validators import test_connection_database
from config.config import Config
from sqlalchemy import text

obter_dados_booking = Blueprint('obter_dados_booking', __name__)
registrar_prestacking_cheio = Blueprint('registrar_prestacking_cheio', __name__)

engine = test_connection_database(Config.DATABASE_URI)

@obter_dados_booking.route('/obter_dados_booking', methods=['GET'])
def obter_dados_booking_endpoint():
    """
    Endpoint para obter dados de booking dos containers.
    ---
    parameters:
      - name: CODIGO
        in: query
        type: string
        required: true
        description: Código do processo para buscar os containers.
    responses:
      200:
        description: Dados dos containers com informações do booking e armador.
        schema:
          type: array
          items:
            type: object
            properties:
              container:
                type: string
              booking:
                type: string
              armador:
                type: string
              response:
                type: object
      400:
        description: Parâmetro 'CODIGO' é obrigatório.
      404:
        description: Não foi encontrado nenhum controle ou container com o código fornecido.
      500:
        description: Erro interno do servidor.
    """
    try:
        codigo = request.args.get('CODIGO')

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

@registrar_prestacking_cheio.route('/registrar_prestacking_cheio', methods=['GET'])
def registrar_prestacking_cheio_endpoint():
    """
    Endpoint para registrar dados de prestacking.
    ---
    parameters:
      - name: CODIGO
        in: query
        type: string
        required: true
        description: Código do processo para buscar os containers.
    responses:
      200:
        description: Dados dos containers com informações do booking e armador.
        schema:
          type: array
          items:
            type: object
            properties:
              container:
                type: string
              booking:
                type: string
              armador:
                type: string
              response:
                type: object
      400:
        description: Parâmetro 'CODIGO' é obrigatório.
      404:
        description: Não foi encontrado nenhum controle ou container com o código fornecido.
      500:
        description: Erro interno do servidor.
    """
    try:
        codigo = request.args.get('CODIGO')

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
                SELECT BOOKING, ARMADOR, CONTAINER, EMAIL_CLIENTE, CODIGO_VERIFICADOR_BOOKING,
                       CNPJ_EXPORTADOR, CONTAINER, PESO_LIQUIDO, TARA, NCM, TIPO_FRETE,
                       ISO, LACRE_ARMADOR, LACRE_SIF, NUMERO_SIF, MODAL, PESAGEM,
                       TEMPERATURA, UMIDADE, VENTILACAO
                FROM containers_processos 
                WHERE flag = 'S' AND COD_CONTROLE_PROCESSO = :codigo
            """), {'codigo': codigo})
            conteiners = [dict(row) for row in result.mappings()]

        if not conteiners:
            return jsonify({"error": "Nenhum contêiner com flag 'S' encontrado."}), 404
        
        client = get_soap_client(Config.WSDL_URL_PRESTACKING)
        response_data = []

        for c in conteiners:
            dados_exportacao = {
                "Armador": c.get("ARMADOR") or "",
                "Booking": c.get("BOOKING") or "",
                "Email": c.get("EMAIL_CLIENTE") or "",
                "CodigoVerificacaoBooking": c.get("CODIGO_VERIFICADOR_BOOKING") or "null",
                "ListaConteineres": [
                    {
                        "UnidadeExportacaoCheio": {
                            "CnpjExportador": c.get("CNPJ_EXPORTADOR"),
                            "NumeroConteiner": c.get("CONTAINER"),
                            "PesoLiquido": c.get("PESO_LIQUIDO") or "null",
                            "Tara": c.get("TARA") or "null",
                            "Ncm": c.get("NCM") or "null",
                            "TipoFrete": c.get("TIPO_FRETE"),
                            "Iso": c.get("ISO") or "null",
                            "LacreArmador": c.get("LACRE_ARMADOR") or "null",
                            "LacreSif": c.get("LACRE_SIF"),
                            "NumeroSif": c.get("NUMERO_SIF"),
                            "Modal": c.get("MODAL") or "null",
                            "PesagemVgm": c.get("PESAGEM") or "null", 
                            "Temperatura": c.get("TEMPERATURA"), 
                            "Umidade": c.get("UMIDADE"),
                            "Ventilacao": c.get("VENTILACAO"),
                            "ListaNotasFiscais": [
                                {
                                    "NFe": {
                                        "ChaveAcesso": "4118097609373100078"  # Uma hora devera pegar do banco
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
            lista_nfe = {
                "NFe": [{
                    "XmlNfe": "00934903",
                    "QuantidadeConteineres": 1
                }]
            }

            body = {
                "ListaNFe": lista_nfe,
                "DadosExportacao": dados_exportacao
            }

            response = call_soap_service(client, "RegistrarPrestackingCheio", **body)        
            response_data.append({
                "response": response
            })
            
        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500