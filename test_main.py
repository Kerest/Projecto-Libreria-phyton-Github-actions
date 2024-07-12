import pytest
from main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_getCliente(client):
    response = client.get('/cliente')
    json_data = response.get_json()
    assert response.status_code == 200
    