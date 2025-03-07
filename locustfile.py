from locust import HttpUser, task, between

class MinhaAPITest(HttpUser):
    wait_time = between(1, 3)

    @task
    def test_minha_api(self):
        payload = {
            "DataInicio": "2025-08-02",
            "DataFinal": "2025-08-02"
        }
        headers = {"Content-Type": "application/json"}
        response = self.client.post("/consulta_navio", json=payload, headers=headers)
        
        if response.status_code != 200:
            response.failure(f"Falha na requisição! Código: {response.status_code}")
