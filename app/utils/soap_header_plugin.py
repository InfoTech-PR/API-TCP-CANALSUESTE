from zeep.plugins import Plugin
from lxml import etree

class CustomHeaderPlugin(Plugin):
    def __init__(self, empresa_selecionada):
        self.empresa_selecionada = empresa_selecionada

    def egress(self, envelope, http_headers, operation, binding_options):
        nsmap = {"wsc": "http://wsclientes.tcp.com.br"}
        header_element = etree.Element("{http://wsclientes.tcp.com.br}RequestHeader", nsmap=nsmap)
        empresa_element = etree.Element("{http://wsclientes.tcp.com.br}EmpresaSelecionada", nsmap=nsmap)
        empresa_element.text = self.empresa_selecionada
        header_element.append(empresa_element)

        header = envelope.find("{http://schemas.xmlsoap.org/soap/envelope/}Header")
        if header is None:
            header = etree.Element("{http://schemas.xmlsoap.org/soap/envelope/}Header")
            envelope.insert(0, header)

        header.append(header_element)
        return envelope, http_headers
