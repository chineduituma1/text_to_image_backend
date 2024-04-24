from fastapi.testclient import TestClient

from main import app
from unittest.mock import patch, MagicMock

import services,schemas

client = TestClient(app)

def test_test_endpoint():
    response = client.get("/", headers={"JWT_SECRET": "myjwtsecret"})
    assert response.status_code == 200
    assert response.json() == {
        "message": " This is a Root endpoint for test purposes. ",
    }

def test_create_user():
    user_data = {
        "email": "alex@example.com",
        "hashed_password": "testpassword",
    }
    response = client.post("/api/create_user", json=user_data)
    assert response.status_code == 200
    created_user = response.json()
    assert created_user["email"] == user_data["email"]
    existing_user_data = {
        "email": "alex@example.com", 
        "hashed_password": "anotherpassword",
    }
    response = client.post("/api/create_user", json=existing_user_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already exists"}

def test_delete_user():
    user_id = "siri@example.com" 
    response = client.delete(f"/api/delete_user/?user_id={user_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}

    non_existent_user_id = "nonexistentuser" 
    response = client.delete(f"/api/delete_user/?user_id={non_existent_user_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_generate_token():
    # Test with valid credentials
    valid_form_data = {
        "username": "testuser@lincs.com",
        "password": "testpassword"
    }
    response = client.post("/api/token", data=valid_form_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

    # Test with invalid credentials
    invalid_form_data = {
        "username": "invalid_username",
        "password": "invalid_password"
    }
    response = client.post("/api/token", data=invalid_form_data)
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid Credentials"}


def test_get_user():
    reg_user = schemas.User(email="testuser@lincs.com", id=1)
    def mock_get_current_user():
        return reg_user
    app.dependency_overrides[services.get_current_user] = mock_get_current_user
    response = client.get("/api/user/me")
    assert response.status_code == 200
    assert response.json() == reg_user.model_dump()
    assert schemas.User(**response.json()) == reg_user
def teardown():
    app.dependency_overrides.clear()

@patch("requests.post")
def test_generate_image(mock_post):
    # Mocking the response from the external API
    expected_image_url = "https://example.com/image.png"
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"url": expected_image_url}]}
    mock_post.return_value = mock_response

    # Make a request to the endpoint
    request_data = {"text": "a red car", "n": 1}
    response = client.post("/api/text", json=request_data)

    # Check that the request to the external API was made with the correct data
    mock_post.assert_called_once_with(
        'https://api.openai.com/v1/images/generations',
        headers={"Authorization": "Bearer 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", "Content-Type": "application/json"},
        json={"prompt": "a red car", "n": 1, "quality": "hd", "size": "1024x1024", "model": "dall-e-3"}
    )

    # Check the response from the endpoint
    assert response.status_code == 200
    assert response.json() == {"url": expected_image_url}
