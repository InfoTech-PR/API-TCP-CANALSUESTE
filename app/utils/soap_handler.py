from flask import jsonify
from zeep import helpers
from zeep.exceptions import Fault
from lxml import etree

def call_soap_service(client, method_name, **params):
    try:
        service_method = getattr(client.service, method_name)  # Obtém o método dinamicamente
        response = service_method(**params)  # Chama o método SOAP

        response_dict = helpers.serialize_object(response)  # Converte para JSON

        return jsonify(response_dict)  # Retorna um JSON válido

    except Fault as fault:
        error_dict = {"error": fault.message}

        if hasattr(fault, "detail") and fault.detail is not None:
            if isinstance(fault.detail, etree._Element):  
                error_dict["detail"] = fault.detail.xpath("string()").strip() 
            else:
                error_dict["detail"] = str(fault.detail)

        return jsonify(error_dict), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
