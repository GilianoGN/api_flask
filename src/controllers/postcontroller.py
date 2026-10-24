from flask import Blueprint, request
from src.models import db, Post
from src.utils import requires_role
from http import HTTPStatus
from sqlalchemy import inspect
from flask_jwt_extended import jwt_required

app = Blueprint("post", __name__, url_prefix="/posts")

@app.route("/", methods=["POST"])
@jwt_required()
@requires_role("normal")
def create_post():
    data = request.json

    if not data or not data.get("author_id") or not all(k in data for k in ("title", "body")):
        return {"error": "Dados incompletos para criação do post."}, HTTPStatus.BAD_REQUEST

    try:
        post = Post(
            author_id=data["author_id"],
            title=data["title"],
            body=data["body"],
        )
        db.session.add(post)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": "Erro ao salvar o post no banco de dados."}, HTTPStatus.INTERNAL_SERVER_ERROR

    return {"message": "Post created!"}, HTTPStatus.CREATED

@app.route("/", methods=["GET"])
@jwt_required()
@requires_role("visitante")
def list_post():
    query = db.select(Post)
    posts = db.session.execute(query).scalars()
    list = [
        {
            "id": post.id,
            "author_id":post.author_id,
            "created":post.created,
            "title":post.title,
            "body":post.body,
        }
        for post in posts
    ]

    return {"posts": list}, HTTPStatus.OK

@app.route("/<int:post_id>")
@jwt_required()
@requires_role("visitante")
def get_post(post_id):
    post = db.get_or_404(Post, post_id)
    return {
        "id": post.id,
        "author_id":post.author_id,
        "created":post.created,
        "title":post.title,
        "body":post.body,
    }

@app.route("/<int:post_id>", methods=["PATCH"])
@jwt_required()
@requires_role("normal")
def update_post(post_id):
    post = db.get_or_404(Post, post_id)
    data = request.json

    mapper = inspect(Post)
    for column in mapper.attrs:
        if column.key in data:
            setattr(post, column.key, data[column.key])
    db.session.commit()

    return {
        "id": post.id,
        "author_id":post.author_id,
        "created":post.created,
        "title":post.title,
        "body":post.body,
    }

@app.route("/<int:post_id>", methods=["DELETE"])
@jwt_required()
@requires_role("normal")
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT