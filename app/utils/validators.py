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

def validar_parametros_banco(container_data, parametros):
    parametros_invalidos = []

    for param in parametros:
        if not container_data.get(param):
            parametros_invalidos.append(param)

    if parametros_invalidos:
        return jsonify({
            "error": "Os seguintes parâmetros estão inválidos (vazios ou nulos):",
            "parametros_invalidos": parametros_invalidos
        }), 400

    return None

def test_connection(database_uri):
    """
    Testa a conexão com o banco de dados usando SQLAlchemy.
    
    :param database_uri: URI de conexão do banco de dados.
    :return: Mensagem indicando sucesso ou erro.
    """
    try:
        engine = create_engine(database_uri)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("✅ Conexão bem-sucedida!")
            return engine
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False
