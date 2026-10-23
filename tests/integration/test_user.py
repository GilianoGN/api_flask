from http import HTTPStatus
from src.app import Role, User, db
from sqlalchemy import func

def test_create_user(client, access_token_admin):
    # Given
    role_id = db.session.execute(db.select(Role.id).where(Role.name == "admin")).scalar()
    payload = {"username":"giliano", "password":"gil123", "active":True, "role_id":role_id}

    # When
    response = client.post("/users/", json=payload, headers={"Authorization": f"Bearer {access_token_admin}"})

    # Then
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"message": "User created!"}
    assert db.session.execute(db.select(func.count(User.id))).scalar() == 4

def test_list_users(client, access_token_normal):
    # Given
    user1 = db.session.execute(db.select(User).where(User.username == "admin-user")).scalar()
    user2 = db.session.execute(db.select(User).where(User.username == "john-doe")).scalar()
    user3 = db.session.execute(db.select(User).where(User.username == "isaac-fer")).scalar()

    # When
    response = client.get("/users/", headers={"Authorization": f"Bearer {access_token_normal}"})

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "users": [
            {
                "id": user1.id,
                "username":user1.username,
                "active":user1.active,
                "role":{
                    "id": user1.role.id,
                    "name": user1.role.name,
                },
            },
            {
                "id": user2.id,
                "username":user2.username,
                "active":user2.active,
                "role":{
                    "id": user2.role.id,
                    "name": user2.role.name,
                },
            },
            {
                "id": user3.id,
                "username":user3.username,
                "active":user3.active,
                "role":{
                    "id": user3.role.id,
                    "name": user3.role.name,
                },
            },
        ]
    }

def test_get_user_success(client, access_token_admin):
    # Given
    user = db.session.execute(db.select(User).where(User.username == "john-doe")).scalar()

    # When
    response = client.get(f"/users/{user.id}", headers={"Authorization": f"Bearer {access_token_admin}"})

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "id": user.id,
        "username": user.username,
        "active":user.active,
        "role":{
            "id": user.role.id,
            "name": user.role.name,
        },
        "password":user.password,
    }

def test_get_user_not_found(client, access_token_admin):
    # Given
    user_id = 999

    # When
    response = client.get(f"/users/{user_id}", headers={"Authorization": f"Bearer {access_token_admin}"})

    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND

def test_delete_user_success(client, access_token_admin):
    # Given
    user = db.session.execute(db.select(User).where(User.username == "john-doe")).scalar()

    # When
    response = client.delete(f"/users/{user.id}", headers={"Authorization": f"Bearer {access_token_admin}"})

    # Then
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert db.session.execute(db.select(func.count(User.id))).scalar() == 2

def test_visitante_nao_pode_criar_usuario(client, access_token_visitante):
    # Given
    role_id = db.session.execute(db.select(Role.id).where(Role.name == "visitante")).scalar()
    payload = {"username":"giliano", "password":"gil123", "active":True, "role_id":role_id}

    # When
    response = client.post("/users/", json=payload, headers={"Authorization": f"Bearer {access_token_visitante}"})

    # Then
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json == {"message": "User dont have access."}
