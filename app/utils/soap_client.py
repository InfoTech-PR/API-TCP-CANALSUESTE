from zeep import Client
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
import requests
from config.config import Config

def get_soap_client(url):
    auth = HTTPBasicAuth(Config.USERNAME, Config.PASSWORD)
    session = requests.Session()
    session.auth = auth
    transport = Transport(session=session)
    client = Client(url, transport=transport)
    return client
