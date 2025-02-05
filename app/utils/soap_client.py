from zeep import Client, Settings
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
import requests
from config.config import Config
from app.utils.soap_header_plugin import CustomHeaderPlugin

def get_soap_client(url, empresa=None):
    auth = HTTPBasicAuth(Config.USERNAME, Config.PASSWORD)
    session = requests.Session()
    session.auth = auth
    transport = Transport(session=session)
    settings = Settings(strict=False, xml_huge_tree=True)
    
    plugins = []
    if empresa:
        plugins.append(CustomHeaderPlugin(empresa))
    
    client = Client(url, transport=transport, settings=settings, plugins=plugins)
    return client
