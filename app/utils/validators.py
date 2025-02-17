from flask import jsonify
from sqlalchemy import create_engine, text

def validar_parametros_obrigatorios(data, parametros_obrigatorios):
    """
    Verifica se os parâmetros obrigatórios estão presentes no JSON da requisição.

    :param data: O JSON recebido na requisição (request.json)
    :param parametros_obrigatorios: Lista de parâmetros que devem estar presentes
    :return: Retorna None se todos os parâmetros estiverem presentes, caso contrário, retorna um JSON de erro.
    """
    parametros_faltantes = [param for param in parametros_obrigatorios if not data.get(param)]

    if parametros_faltantes:
        return jsonify({
            "error": "Os seguintes parâmetros são obrigatórios:",
            "parametros_faltantes": parametros_faltantes
        }), 400

    return None 

def get_database_engine(database_uri):
    return create_engine(
        database_uri,
        pool_recycle=3600, 
        pool_pre_ping=True
    )