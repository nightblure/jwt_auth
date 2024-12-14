from typing import Any

from starlette.testclient import TestClient


def test_register_success(api_client: TestClient, existed_user_register_data: dict[str, Any]) -> None:
    response = api_client.post("/auth/register", json=existed_user_register_data)

    assert response.status_code == 201


def test_register_fail_on_conflict(api_client: TestClient, existed_user_register_data: dict[str, Any]) -> None:
    response = api_client.post("/auth/register", json=existed_user_register_data)

    assert response.status_code == 409


def test_login_success(api_client: TestClient, existed_user_register_data: dict[str, Any]) -> None:
    response = api_client.post("/auth/login", json=existed_user_register_data)

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_user_not_found(api_client: TestClient) -> None:
    response = api_client.post(
        "/auth/login",
        json={"email": "sr23r23@gmail.com", "password": "1234tydf"},
    )

    assert response.status_code == 404


def test_login_fail_with_incorrect_password(api_client: TestClient, existed_user_register_data: dict[str, Any]) -> None:
    existed_user_register_data["password"] = "sdf2frnd"

    response = api_client.post("/auth/login", json=existed_user_register_data)

    assert response.status_code == 401


def test_me_success(api_client: TestClient, existed_user_register_data: dict[str, Any]) -> None:
    response = api_client.post("/auth/login", json=existed_user_register_data)
    response.raise_for_status()
    access_token = response.json()["access_token"]

    response = api_client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["email"] == existed_user_register_data["email"]
    assert response_data["username"] == existed_user_register_data["username"]
    assert "logged_in" in response_data


def test_me_fail_with_invalid_token(api_client: TestClient, existed_user_register_data: dict[str, Any]) -> None:
    response = api_client.post("/auth/login", json=existed_user_register_data)
    access_token = response.json()["access_token"] + "random"

    response = api_client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400


def test_full_flow_success(api_client: TestClient, register_data: dict[str, Any]) -> None:
    api_client.post("/auth/register", json=register_data)
    access_token: str = api_client.post("/auth/login", json=register_data).json()["access_token"]

    response = api_client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["email"] == register_data["email"]
    assert response_data["username"] == register_data["username"]
    assert "logged_in" in response_data
