def test_register_success(api_client, register_data):
    response = api_client.post('/auth/register', json=register_data)
    assert response.status_code == 201


def test_register_conflict(api_client, existed_user_register_data):
    response = api_client.post('/auth/register', json=existed_user_register_data)
    assert response.status_code == 409


def test_docs_available(api_client):
    assert api_client.get('/docs').status_code == 200


def test_login_success(api_client, existed_user_login_data):
    response = api_client.post('/auth/login', json=existed_user_login_data)

    assert response.status_code == 200
    assert 'access_token' in response.json()


def test_login_user_not_found(api_client):
    response = api_client.post('/auth/login', json={'email': 'sr23r23@gmail.com', 'password': '1234tydf'})
    assert response.status_code == 404
