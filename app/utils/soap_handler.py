from collections import deque
from flask import jsonify
from zeep import helpers
from zeep.exceptions import Fault
from lxml import etree
import xml.etree.ElementTree as ET

def call_soap_service(client, method_name, **params):
    try:
        service_method = getattr(client.service, method_name)
        response = service_method(**params)
        response_dict = helpers.serialize_object(response)

        if '_raw_elements' in response_dict:
            raw_elements = response_dict['_raw_elements']
            for element in raw_elements:
                if element.tag.endswith('Armador'):
                    response_dict['Armador'] = element.text
                elif element.tag.endswith('Booking'):
                    response_dict['Booking'] = element.text
                elif element.tag.endswith('NomeNavio'):
                    response_dict['NomeNavio'] = element.text
                elif element.tag.endswith('Viagem'):
                    response_dict['Viagem'] = element.text
                elif element.tag.endswith('PortoDescarga'):
                    response_dict['PortoDescarga'] = element.text
                elif element.tag.endswith('PortoDestino'):
                    response_dict['PortoDestinoFinal'] = element.text
                elif element.tag.endswith('CodigoVerificacaoBooking'):
                    response_dict['CodigoVerificacaoBooking'] = element.text
                elif element.tag.endswith('ListaISO'):
                    response_dict['ListaIso'] = [iso.text for iso in element.findall('.//wsc:ISO', namespaces={'wsc': 'http://wsclientes.tcp.com.br'})]
                elif element.tag.endswith('RetornoValidacao'):
                    response_dict['RetornoValidacao'] = {
                        'IndicadorErro': element.findtext('.//wsc:IndicadorErro', namespaces={'wsc': 'http://wsclientes.tcp.com.br'}),
                        'ListaMensagemRetornoWs': [
                            {
                                'Codigo': msg.findtext('.//wsc:Codigo', namespaces={'wsc': 'http://wsclientes.tcp.com.br'}),
                                'Mensagem': msg.findtext('.//wsc:Mensagem', namespaces={'wsc': 'http://wsclientes.tcp.com.br'})
                            }
                            for msg in element.findall('.//wsc:MensagemRetornoWs', namespaces={'wsc': 'http://wsclientes.tcp.com.br'})
                        ]
                    }

            if '_raw_elements' in response_dict:
                del response_dict['_raw_elements']
        
        return jsonify(response_dict)

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
