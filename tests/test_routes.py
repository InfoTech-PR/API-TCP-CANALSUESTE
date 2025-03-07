import requests

base_url = "http://127.0.0.1:3002"

def test_obter_dados_booking():
    params = {"CODIGO": 16}
    response = requests.get(f"{base_url}/obter_dados_booking", params=params)
    assert response.status_code == 200, f"Esperado 200, mas obteve {response.status_code}"

def test_consulta_navio():
    data = {
        "DataInicio": "2025-08-02",
        "DataFinal": "2025-08-02"
    }
    response = requests.post(f"{base_url}/consulta_navio", json=data)
    assert response.status_code == 200, f"Esperado 200, mas obteve {response.status_code}"