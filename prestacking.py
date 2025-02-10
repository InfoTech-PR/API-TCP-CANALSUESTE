import requests

url_dados_booking = 'http://85.31.63.241:3002/obter_dados_booking'
url_registrar_prestacking_cheio = 'http://85.31.63.241:3002/registrar_prestacking_cheio'
data = {
    "CODIGO": "16"
}

response = requests.get(url_registrar_prestacking_cheio, json=data)
response_json = response.json()

if response_json:
    print(response_json)
else:
    print("Lista vazia ou resposta inesperada")
