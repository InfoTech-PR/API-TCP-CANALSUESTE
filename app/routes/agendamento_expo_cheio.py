from flask import Blueprint, request, jsonify
from app.utils.soap_client import get_soap_client
from app.utils.soap_handler import call_soap_service
from config.config import Config

agendar_unidade = Blueprint('agendar_unidade', __name__)
consultar_grade = Blueprint('consultar_grade', __name__)
editar_agenda_unidade = Blueprint('editar_agenda_unidade', __name__)
deletar_agenda_unidade = Blueprint('deletar_agenda_unidade', __name__)

@agendar_unidade.route('/agendar_unidade', methods=['POST'])
def agendar_unidade_endpoint():
    data = request.json

    data_prevista = data.get('DataPrevista')
    grade_configuracao = data.get('GradeConfiguracao')
    tipo_grade = data.get('TipoGrade')
    transportadora = data.get('Transportadora')
    motorista = data.get('Motorista')
    veiculo_tipo = data.get('VeiculoTipo')
    veiculo_placa_principal = data.get('VeiculoPlacaPrincipal')
    conteiner = data.get('Conteiner')
    placa_reboque1 = data.get('PlacaReboque1')
    placa_reboque2 = data.get('PlacaReboque2')

    if not data_prevista or not grade_configuracao or not tipo_grade or not transportadora or not motorista:
        return jsonify({"error": "Todos os parâmetros são obrigatórios!"}), 400

    client = get_soap_client(Config.WSDL_URL_GRADE)

    return call_soap_service(
        client,
        "AgendarUnidades",
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

@consultar_grade.route('/consultar_grade', methods=['GET'])
def consultar_grade_endpoint():
    data = request.json
    data_prevista = data.get('DataPrevista')

    if not data_prevista:
        return jsonify({"error": "Parâmetro 'DataPrevista' é obrigatório!"}), 400

    client = get_soap_client(Config.WSDL_URL_GRADE)
    return call_soap_service(client, "ConsultarGrades", DataPrevista=data_prevista)

@editar_agenda_unidade.route('/editar_agenda_unidade', methods=['POST'])
def editar_agenda_unidade_endpoint():
    data = request.json

    id_agendamento = data.get('IdAgendamento')
    grade_configuracao = data.get('GradeConfiguracao')
    transportadora = data.get('Transportadora')
    motorista = data.get('Motorista')
    veiculo = data.get('Veiculo')
    conteineres = data.get('Conteineres')
    data_prevista = data.get('DataPrevista')

    if not id_agendamento or not grade_configuracao or not transportadora or not motorista or not veiculo or not conteineres or not data_prevista:
        return jsonify({"error": "Todos os parâmetros são obrigatórios!"}), 400

    client = get_soap_client(Config.WSDL_URL_GRADE)
    return call_soap_service(
        client, "EditarAgendamentoUnidades", 
        IdAgendamento=id_agendamento,
        GradeConfiguracao=grade_configuracao,
        Transportadora=transportadora,
        Motorista=motorista,
        Veiculo={
            'Tipo': veiculo.get('Tipo'),
            'PlacaPrincipal': veiculo.get('PlacaPrincipal'),
            'PlacaReboque1': veiculo.get('PlacaReboque1', ''),
            'PlacaReboque2': veiculo.get('PlacaReboque2', '')
        },
        Conteineres=[{'Conteiner': conteiner} for conteiner in conteineres],
        DataPrevista=data_prevista
    )

@deletar_agenda_unidade.route('/deletar_agenda_unidade', methods=['POST'])
def deletar_agenda_unidade_endpoint():
    data = request.json

    id_agendamento = data.get('IdAgendamento')

    if not id_agendamento:
        return jsonify({"error": "O parâmetro 'IdAgendamento' é obrigatório!"}), 400

    client = get_soap_client(Config.WSDL_URL_GRADE)
    return call_soap_service(client, "ExcluirAgendamentoUnidades", IdAgendamento=id_agendamento)