from http import HTTPStatus
from src.models import db, Post, User
from sqlalchemy import func

def test_create_post_success(client, access_token_normal):
    # Given
    user_id = db.session.execute(db.select(User.id).where(User.username == "john-doe")).scalar()
    payload = {"author_id":user_id, "title":"Teste de postagem", "body":""}

    # When
    response = client.post("/posts/", json=payload, headers={"Authorization": f"Bearer {access_token_normal}"})

    # Then
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"message": "Post created!"}
    assert db.session.execute(db.select(func.count(Post.id))).scalar() == 3

def test_create_post_fail(client, access_token_normal):
    # Given
    payload = {"author_id":"", "title":"Teste de postagem", "body":"Corpo do teste de postagem"}

    # When
    response = client.post("/posts/", json=payload, headers={"Authorization": f"Bearer {access_token_normal}"})

    # Then
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {"error": "Dados incompletos para criação do post."}
    assert db.session.execute(db.select(func.count(Post.id))).scalar() == 2

def test_list_posts(client, access_token_visitante):
    # Given
    user1 = db.session.execute(db.select(User).where(User.username == "admin-user")).scalar()
    user2 = db.session.execute(db.select(User).where(User.username == "isaac-fer")).scalar()
    post1 = db.session.execute(db.select(Post).where(Post.author_id == user1.id)).scalar()
    post2 = db.session.execute(db.select(Post).where(Post.author_id == user2.id)).scalar()

    # When
    response = client.get("/posts/", headers={"Authorization": f"Bearer {access_token_visitante}"})

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "posts": [
            {
                "author_id":post1.author_id,
                "title":post1.title,
                "body":post1.body,
            },
            {
                "author_id":post2.author_id,
                "title":post2.title,
                "body":post2.body,
            },
        ]
    }

def test_get_post_success(client, access_token_normal):
    # Given
    user = db.session.execute(db.select(User).where(User.username == "admin-user")).scalar()
    post = db.session.execute(db.select(Post).where(Post.author_id == user.id)).scalar()

    # When
    response = client.get(f"/posts/{post.id}", headers={"Authorization": f"Bearer {access_token_normal}"})

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        {
            "author_id":post.author_id,
            "title":post.title,
            "body":post.body,
        },
    }

def test_get_post_not_found(client, access_token_normal):
    # Given
    post_id = 999

    # When
    response = client.get(f"/posts/{post_id}", headers={"Authorization": f"Bearer {access_token_normal}"})

    # Then
    assert response.status_code == HTTPStatus.NOT_FOUND

def test_delete_post_success(client, access_token_normal):
    # Given
    user = db.session.execute(db.select(User).where(User.username == "admin-user")).scalar()
    post = db.session.execute(db.select(Post).where(Post.author_id == user.id)).scalar()

    # When
    response = client.delete(f"/posts/{post.id}", headers={"Authorization": f"Bearer {access_token_normal}"})

    # Then
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert db.session.execute(db.select(func.count(Post.id))).scalar() == 1

def test_visitante_nao_pode_criar_post(client, access_token_visitante):
    # Given
    user_id = db.session.execute(db.select(User.id).where(User.username == "john-doe")).scalar()
    payload = {"author_id":user_id, "title":"Teste de postagem", "body":"Corpo do teste de postagem"}

    # When
    response = client.post("/posts/", json=payload, headers={"Authorization": f"Bearer {access_token_visitante}"})

    # Then
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json == {"message": "User dont have access."}
