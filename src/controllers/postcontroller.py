from flask import Blueprint, request
from src.models import db, Post
from src.utils import requires_role
from src.views.postview import PostSchemaAll, CreatePostSchema
from http import HTTPStatus
from sqlalchemy import inspect # type: ignore
from flask_jwt_extended import jwt_required # type: ignore
from marshmallow import ValidationError # type: ignore

app = Blueprint("post", __name__, url_prefix="/posts")

@app.route("/", methods=["POST"])
@jwt_required()
@requires_role("normal")
def create_post():
    """Create a post.
    ---
    post:
        tags:
            - post
        summary: Create a new post (Exceto Visitantes)
        description: Creates a new post with author_id, title and body
        requestBody:
            required: true
            content:
                application/json:
                    schema: CreatePostSchema
        responses:
            201:
                description: Post created successfully
            400:
                description: Incomplete data for post creation
            422:
                description: Validation error
        security:
            - BearerAuth: []
    """
    post_schema = CreatePostSchema()

    try:
        data = post_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY

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
    """List post view.
    ---
    get:
        tags:
            - post
        summary: List all post
        description: Retrieves a list of all registered post
        responses:
            200:
                description: Successful operation
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                post:
                                    type: array
                                    items:
                                        Schema: PostSchemaAll
        security:
            - BearerAuth: []
    """
    query = db.select(Post)
    posts = db.session.execute(query).scalars()
    posts_schema = PostSchemaAll(many=True)
    list = posts_schema.dump(posts)

    return {"posts": list}, HTTPStatus.OK

@app.route("/<int:post_id>")
@jwt_required()
@requires_role("visitante")
def get_post(post_id):
    """Post detail view.
    ---
    get:
        tags:
            - post
        summary: Get a post
        description: get a post
        parameters:
            - in: path
              name: post_id
              schema: PostIdParameter
        responses:
            200:
                description: Successful operation
                content:
                    application/json:
                        schema: PostSchemaAll
        security:
            - BearerAuth: []
    """
    post = db.get_or_404(Post, post_id)
    post_schema = PostSchemaAll()
    return post_schema.dump(post), HTTPStatus.OK

@app.route("/<int:post_id>", methods=["PATCH"])
@jwt_required()
@requires_role("normal")
def update_post(post_id):
    """Update a post.
    ---
    patch:
        tags:
            - post
        summary: Update a post partially (Exceto Visitante)
        description: Updates specific fields of an existing post by ID
        parameters:
            - in: path
              name: post_id
              schema: PostIdParameter
        responses:
            200:
                description: Successful operation
                content:
                    application/json:
                        schema: PostSchemaAll
            400:
                description: Post not found
        security:
            - BearerAuth: []
    """
    post = db.get_or_404(Post, post_id)
    data = request.json

    mapper = inspect(Post)
    for column in mapper.attrs:
        if column.key in data:
            setattr(post, column.key, data[column.key])
    db.session.commit()

    post_schema = PostSchemaAll()
    return post_schema.dump(post), HTTPStatus.OK

@app.route("/<int:post_id>", methods=["DELETE"])
@jwt_required()
@requires_role("normal")
def delete_post(post_id):
    """Post delete view.
    ---
    delete:
        tags:
            - post
        summary: Deletes a post (Exceto Visitante)
        description: delete a post
        parameters:
            - in: path
              name: post_id
              schema: PostIdParameter
        responses:
            204:
                description: Seccessful operation
            404:
                description: Not found post
        security:
            - BearerAuth: []
    """
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT

# Lista de view do Post para o APISpec
POST_VIEWS = [
    create_post,
    list_post,
    get_post,
    update_post,
    delete_post
]