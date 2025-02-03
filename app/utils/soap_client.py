from zeep import Client, Settings
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
import requests
from config.config import Config

def get_soap_client(url):
    auth = HTTPBasicAuth(Config.USERNAME, Config.PASSWORD)
    session = requests.Session()
    session.auth = auth
    transport = Transport(session=session)
    settings = Settings(strict=False, xml_huge_tree=True)
    client = Client(url, transport=transport, settings=settings)
    return client
