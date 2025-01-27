from flask import Blueprint, request, jsonify
from app.utils.soap_client import get_soap_client
from config.config import Config

consulta_grade = Blueprint('consulta_grade', __name__)

@consulta_grade.route('/consulta_grade', methods=['GET'])
def consulta_grade_endpoint():
    data_prevista = request.args.get('DataPrevista')

    if not data_prevista:
        return jsonify({"error": "Parâmetro 'DataPrevista' é obrigatório!"}), 400

    client = get_soap_client(Config.WSDL_URL_GRADE)
    try:
        response = client.service.ConsultarGrades(DataPrevista=data_prevista)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
