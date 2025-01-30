from flask import Blueprint, request, jsonify
from app.utils.soap_client import get_soap_client
from config.config import Config

bloqueio_nvo = Blueprint('bloqueio_nvo', __name__)
bloqueio_nvo_master = Blueprint('bloqueio_nvo_master', __name__)
movimentacao_importacao = Blueprint('movimentacao_importacao', __name__)

@bloqueio_nvo.route('/bloqueio_nvo', methods=['POST'])
def bloqueio_nvo_endpoint():
    data = request.json
    ce_master = data.get('CEMaster')
    bl_master = data.get('BLMaster')
    ce_house = data.get('CEHouse')
    bl_house = data.get('BLHouse')
    acao = data.get('Acao')
    
    if not all([ce_master, bl_master, ce_house, bl_house, acao]):
        return jsonify({"error": "Todos os campos são obrigatórios!"}), 400
    
    client = get_soap_client(Config.WSDL_URL_IMPORTACAO)
    try:
        response = client.service.BloqueioNVO(
            CEMaster=ce_master, BLMaster=bl_master, 
            CEHouse=ce_house, BLHouse=bl_house, Acao=acao
        )
        response_dict = to_serializable(response)
        return jsonify(response_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bloqueio_nvo_master.route('/bloqueio_nvo_master', methods=['POST'])
def bloqueio_nvo_master_endpoint():
    data = request.json
    bl_master = data.get('BLMaster')
    
    if not bl_master:
        return jsonify({"error": "O campo 'BLMaster' é obrigatório!"}), 400
    
    client = get_soap_client(Config.WSDL_URL_IMPORTACAO)
    try:
        response = client.service.BloqueioNVOMaster(BLMaster=bl_master)
        response_dict = to_serializable(response)
        return jsonify(response_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@movimentacao_importacao.route('/movimentacao_importacao', methods=['GET'])
def movimentacao_importacao_endpoint():
    data = request.json
    ce_mercante = data.get('CeMercante')
    tipo_operacao = data.get('TipoOperacao')
    data_inicial = data.get('DataInicial')
    data_final = data.get('DataFinal')
    empresa_selecionada = data.get('EmpresaSelecionada')
    
    if not all([ce_mercante, tipo_operacao, data_inicial, data_final, empresa_selecionada]):
        return jsonify({"error": "Todos os campos são obrigatórios!"}), 400
    
    client = get_soap_client(Config.WSDL_URL_IMPORTACAO)
    try:
        response = client.service.ConsultaMovimentacao(
            CeMercante=ce_mercante, TipoOperacao=tipo_operacao,
            DataInicial=data_inicial, DataFinal=data_final
        )
        response_dict = to_serializable(response)
        return jsonify(response_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
