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
            namespace = {'wsc': 'http://wsclientes.tcp.com.br'}

            for element in raw_elements:
                armador = element.find('wsc:Armador', namespaces=namespace)
                booking = element.find('wsc:Booking', namespaces=namespace)
                nome_navio = element.find('wsc:NomeNavio', namespaces=namespace)
                viagem = element.find('wsc:Viagem', namespaces=namespace)
                porto_descarga = element.find('wsc:PortoDescarga', namespaces=namespace)
                porto_destino = element.find('wsc:PortoDestino', namespaces=namespace)
                cod_verificacao = element.find('wsc:CodigoVerificacaoBooking', namespaces=namespace)
                lista_iso = element.find('wsc:ListaISO', namespaces=namespace)

                if armador is not None:
                    response_dict['Armador'] = armador.text
                if booking is not None:
                    response_dict['Booking'] = booking.text
                if nome_navio is not None:
                    response_dict['NomeNavio'] = nome_navio.text
                if viagem is not None:
                    response_dict['Viagem'] = viagem.text
                if porto_descarga is not None:
                    response_dict['PortoDescarga'] = porto_descarga.text
                if porto_destino is not None:
                    response_dict['PortoDestinoFinal'] = porto_destino.text
                if cod_verificacao is not None:
                    response_dict['CodigoVerificacaoBooking'] = cod_verificacao.text
                if lista_iso is not None:
                    response_dict['ListaIso'] = [iso.text for iso in lista_iso.findall('wsc:ISO', namespaces=namespace)]

                retorno_validacao = element.find('wsc:RetornoValidacao', namespaces=namespace)
                if retorno_validacao is not None:
                    indicador_erro = retorno_validacao.find('wsc:IndicadorErro', namespaces=namespace)
                    lista_msg_retorno = retorno_validacao.findall('wsc:ListaMensagemRetornoWs/wsc:MensagemRetornoWs', namespaces=namespace)

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

            if '_raw_elements' in response_dict:
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