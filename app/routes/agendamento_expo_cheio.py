from flask import Blueprint, request, jsonify
from app.utils.soap_client import get_soap_client
from app.utils.soap_handler import call_soap_service
from app.utils.validators import validar_parametros_obrigatorios
from config.config import Config

agendar_unidade = Blueprint('agendar_unidade', __name__)
consultar_grade = Blueprint('consultar_grade', __name__)
editar_agenda_unidade = Blueprint('editar_agenda_unidade', __name__)
deletar_agenda_unidade = Blueprint('deletar_agenda_unidade', __name__)

@agendar_unidade.route('/agendar_unidade', methods=['POST'])
def agendar_unidade_endpoint():
    data = request.json
    parametros_obrigatorios = [
        "GradeConfiguracao", "Transportadora", 
        "Motorista", "VeiculoTipo",
        "Conteineres", "DataPrevista"
        ]

    erro = validar_parametros_obrigatorios(data, parametros_obrigatorios)
    if erro:
        return erro
    client = get_soap_client(Config.WSDL_URL_GRADE)
    return call_soap_service(
            client,
            "AgendarUnidades",
            GradeConfiguracao=data["GradeConfiguracao"],
            TipoGrade=data.get("TipoGrade", ""),
            Transportadora=data["Transportadora"],
            Motorista=data["Motorista"],
            Veiculo={
                "Tipo": data["VeiculoTipo"],
                "PlacaPrincipal": data.get("VeiculoPlacaPrincipal", ""),
                "PlacaReboque1": data.get("PlacaReboque1", ""),
                "PlacaReboque2": data.get("PlacaReboque2", "")
            },
            Conteineres=[{"Conteiner": c} for c in data["Conteineres"]],
            DataPrevista=data["DataPrevista"]
        )

@consultar_grade.route('/consultar_grade', methods=['POST'])
def consultar_grade_endpoint():
    data = request.json
    
    data_prevista = data.get('DataPrevista')
    
    if not data_prevista:
        return jsonify({"error": "O parâmetro 'DataPrevista' é obrigatório!"}), 400
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