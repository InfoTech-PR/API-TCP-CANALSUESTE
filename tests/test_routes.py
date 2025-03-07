import requests

base_url = "http://200.98.204.251:3002"

def test_obter_dados_booking():
    params = {"CODIGO": 16}
    response = requests.get(f"{base_url}/obter_dados_booking", params=params)
    assert response.status_code == 200, f"Esperado 200, mas obteve {response.status_code}"

def test_registrar_prestacking_cheio():
    params = {"CODIGO": 16}
    response = requests.get(f"{base_url}/obter_dados_booking", params=params)
    assert response.status_code == 200, f"Esperado 200, mas obteve {response.status_code}"