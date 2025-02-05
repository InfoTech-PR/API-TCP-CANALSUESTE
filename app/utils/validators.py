from flask import jsonify

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
