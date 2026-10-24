import pytest
from src.app import create_app, bcrypt
from src.models import db, Role, User, Post

@pytest.fixture()
def app():
    app = create_app(environment="testing")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def populate_db(app):

    hashed_password = bcrypt.generate_password_hash("test").decode("utf-8")

    role1 = Role(name="admin")
    role2 = Role(name="normal")
    role3 = Role(name="visitante")
    db.session.add_all([role1, role2, role3])
    db.session.commit()

    user1 = User(username="admin-user", password=hashed_password, active=True, role_id=role1.id)
    user2 = User(username="john-doe", password=hashed_password, active=True, role_id=role1.id)
    user3 = User(username="isaac-fer", password=hashed_password, active=True, role_id=role2.id)
    db.session.add_all([user1, user2, user3])
    db.session.commit()

    post1 = Post(author_id=user1.id, title="Titulo da postagem 1", body="Corpo do teste de postagem")
    post2 = Post(author_id=user3.id, title="Titulo da postagem 2", body="Corpo do teste de postagem")
    db.session.add_all([post1, post2])
    db.session.commit()

@pytest.fixture()
def access_token_admin(client):
    user = db.session.execute(db.select(User).where(User.username == "admin-user")).scalar()
    response = client.post("/auth/login", json={"username": user.username, "password": "test"})
    return response.json["access_token"]

@pytest.fixture()
def access_token_normal(client):
    user = db.session.execute(db.select(User).where(User.username == "isaac-fer")).scalar()
    response = client.post("/auth/login", json={"username": user.username, "password": "test"})
    return response.json["access_token"]

@pytest.fixture()
def access_token_visitante(client):
    role3 = db.session.execute(db.select(Role).where(Role.name == "visitante")).scalar()
    hashed_password = bcrypt.generate_password_hash("test").decode("utf-8")

    user = User(username="visitante-user", password=hashed_password, active=False, role_id=role3.id)
    db.session.add(user)
    db.session.commit()
    
    response = client.post("/auth/login", json={"username": user.username, "password": "test"})
    return response.json["access_token"]
