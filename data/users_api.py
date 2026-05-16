import flask
import data.db_session as db_session
from flask import jsonify, make_response, request
from .users import User

blueprint = flask.Blueprint("users_api", __name__, template_folder="templates")


@blueprint.route("/api/users")
def get_users():
    users = db_session.db_sess.query(User).all()
    return jsonify(
        {
            "users": [
                item.to_dict(only=("name", "email", "created_date", "image"))
                for item in users
            ]
        }
    )


@blueprint.route("/api/users/<int:user_id>")
def get_user(user_id):
    user = db_session.db_sess.get(User, user_id)
    if not user:
        return make_response(jsonify({"error": "Not Found"}), 404)
    return jsonify(
        {"user": user.to_dict(only=("name", "email", "created_date", "image"))}
    )


@blueprint.route("/api/users", methods=["POST"])
def create_user():
    if not request.json:
        return make_response(jsonify({"error": "Empty request"}), 400)
    elif not all(key in request.json for key in ["name", "email", "password"]):
        return make_response(jsonify({"error": "Bad request"}), 400)
    user = User()
    user.set_password(request.json["password"])
    user.name = request.json["name"]
    user.email = request.json["email"]
    db_session.db_sess.add(user)
    db_session.db_sess.commit()
    return jsonify({"id": user.id})