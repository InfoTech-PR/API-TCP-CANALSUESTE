from flask import Blueprint, request, jsonify
from app.utils.soap_client import get_soap_client
from config.config import Config

agenda_unidade = Blueprint('agenda_unidade', __name__)

@agenda_unidade.route('/agenda_unidade', methods=['GET'])
def agenda_unidade_endpoint():
    data_prevista = request.args.get('DataPrevista')
    grade_configuracao = request.args.get('GradeConfiguracao')
    tipo_grade = request.args.get('TipoGrade')
    transportadora = request.args.get('Transportadora')
    motorista = request.args.get('Motorista')
    veiculo_tipo = request.args.get('VeiculoTipo')
    veiculo_placa_principal = request.args.get('VeiculoPlacaPrincipal')
    conteiner = request.args.get('Conteiner')

    if not data_prevista or not grade_configuracao or not tipo_grade or not transportadora or not motorista:
        return jsonify({"error": "Todos os parâmetros são obrigatórios!"}), 400

    placa_reboque1 = request.args.get('PlacaReboque1', '')
    placa_reboque2 = request.args.get('PlacaReboque2', '')

    client = get_soap_client(Config.WSDL_URL_GRADE)

    try:
        response = client.service.AgendarUnidades(
            GradeConfiguracao=grade_configuracao,
            TipoGrade=tipo_grade,
            Transportadora=transportadora,
            Motorista=motorista,
            Veiculo={
                'Tipo': veiculo_tipo,
                'PlacaPrincipal': veiculo_placa_principal,
                'PlacaReboque1': placa_reboque1,
                'PlacaReboque2': placa_reboque2
            },
            Conteineres=[{'Conteiner': conteiner}],
            DataPrevista=data_prevista
        )
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
