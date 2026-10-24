from flask import jsonify
from sqlalchemy.exc import IntegrityError
from http import HTTPStatus

def register_error_hadlers(app):
    @app.errorhandler(KeyError)
    def hadle_key_error(e):
        return jsonify({"error": f"Campo obrigatório ausente: {e}"}), HTTPStatus.BAD_REQUEST

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(e):
        app.db.session.rollback()
        return jsonify({"error": "Erro de integridade no banco de dados (possível duplicidade de registro)."}), HTTPStatus.BAD_REQUEST

    @app.errorhandler(400)
    def handle_bad_request(e):
        return jsonify({"error": "Requisição inválida ou mal formatada."}), HTTPStatus.BAD_REQUEST
