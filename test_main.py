from fastapi.testclient import TestClient

from main import app

import services,schemas

client = TestClient(app)

def test_test_endpoint():
    response = client.get("/", headers={"JWT_SECRET": "myjwtsecret"})
    assert response.status_code == 200
    assert response.json() == {
        "message": "Root endpoint",
    }


def test_get_user():
    reg_user = schemas.User(email="testuser@lincs.com", id=1)
    reg_user = schemas.User(email="chineduracks1@lincs.com", id=2)
    def mock_get_current_user():
        return reg_user
    app.dependency_overrides[services.get_current_user] = mock_get_current_user
    response = client.get("/user/me")
    assert response.status_code == 200
    assert response.json() == reg_user.dict()
    assert schemas.User(**response.json()) == reg_user
def teardown():
    app.dependency_overrides.clear()
