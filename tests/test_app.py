from http import HTTPStatus


def test_root_debe_retornar_hola_mundo(client):
    # client = TestClient(app)  # Organizar

    response = client.get('/')  # actuar

    assert response.status_code == HTTPStatus.OK  # afirmar
    assert response.json() == {'message': 'hola mundo!'}  # afirmar
