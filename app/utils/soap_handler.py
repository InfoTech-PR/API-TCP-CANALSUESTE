from flask import logging
from zeep import helpers
from zeep.exceptions import Fault
from lxml import etree

def call_soap_service(client, method_name, **params):
    try:
        service_method = getattr(client.service, method_name)
        response = service_method(**params)
        response_dict = helpers.serialize_object(response)

        if '_raw_elements' in response_dict:
            raw_elements = response_dict['_raw_elements']
            namespace = {'wsc': 'http://wsclientes.tcp.com.br'}
            
            for element in raw_elements:
                tag_name = etree.QName(element).localname  # Obtém o nome do elemento sem namespace
                if tag_name == 'Armador':
                    response_dict['Armador'] = element.text
                elif tag_name == 'Booking':
                    response_dict['Booking'] = element.text
                elif tag_name == 'NomeNavio':
                    response_dict['NomeNavio'] = element.text
                elif tag_name == 'Viagem':
                    response_dict['Viagem'] = element.text
                elif tag_name == 'PortoDescarga':
                    response_dict['PortoDescarga'] = element.text
                elif tag_name == 'PortoDestino':
                    response_dict['PortoDestinoFinal'] = element.text
                elif tag_name == 'CodigoVerificacaoBooking':
                    response_dict['CodigoVerificacaoBooking'] = element.text
                elif tag_name == 'ListaISO':
                    response_dict['ListaIso'] = [iso.text for iso in element.findall('wsc:ISO', namespaces=namespace)]
                elif tag_name == 'RetornoValidacao':
                    indicador_erro = element.find('wsc:IndicadorErro', namespaces=namespace)
                    lista_msg_retorno = element.findall('wsc:ListaMensagemRetornoWs/wsc:MensagemRetornoWs', namespaces=namespace)
                    response_dict['RetornoValidacao'] = {
                        'IndicadorErro': indicador_erro.text if indicador_erro is not None else None,
                        'ListaMensagemRetornoWs': [
                            {
                                'Codigo': msg.findtext('wsc:Codigo', namespaces=namespace),
                                'Mensagem': msg.findtext('wsc:Mensagem', namespaces=namespace)
                            }
                            for msg in lista_msg_retorno
                        ]
                    }
            
            del response_dict['_raw_elements']
        
        return response_dict  

    except Fault as fault:
        error_dict = {"error": fault.message}
        if hasattr(fault, "detail") and fault.detail is not None:
            if isinstance(fault.detail, etree._Element):  
                error_dict["detail"] = fault.detail.xpath("string()").strip() 
            else:
                error_dict["detail"] = str(fault.detail)
        return error_dict  
    except Exception as e:
        return {"error": str(e)}
