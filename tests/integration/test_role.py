from http import HTTPStatus
from src.app import Role, User, db
from sqlalchemy import func

def test_create_role(client, access_token_admin):
    # Given
    payload = {"name":"gerencia"}

    # When
    response = client.post("/roles/", json=payload, headers={"Authorization": f"Bearer {access_token_admin}"})

    # Then
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"message": "Role created!"}
    assert db.session.execute(db.select(func.count(Role.id))).scalar() == 4

def test_list_roles(client, access_token_normal):
    # Given
    role1 = db.session.execute(db.select(Role).where(Role.name == "admin")).scalar()
    role2 = db.session.execute(db.select(Role).where(Role.name == "normal")).scalar()
    role3 = db.session.execute(db.select(Role).where(Role.name == "visitante")).scalar()

    # When
    response = client.get("/roles/", headers={"Authorization": f"Bearer {access_token_normal}"})

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "roles": [
            {
                "id": role1.id,
                "name":role1.name,
            },
            {
                "id": role2.id,
                "name": role2.name,
            },
            {
                "id": role3.id,
                "name": role3.name,
            },
        ]
    }

def test_delete_role_success(client, access_token_admin):
    # Given
    role = db.session.execute(db.select(Role).where(Role.name == "visitante")).scalar()

    # When
    response = client.delete(f"/roles/{role.id}", headers={"Authorization": f"Bearer {access_token_admin}"})

    # Then
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert db.session.execute(db.select(func.count(Role.id))).scalar() == 2

def test_delete_role_fail(client, access_token_admin):
    # Given
    role = db.session.execute(db.select(Role).where(Role.name == "normal")).scalar()

    # When
    response = client.delete(f"/roles/{role.id}", headers={"Authorization": f"Bearer {access_token_admin}"})

    # Then
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
