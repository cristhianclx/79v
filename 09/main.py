from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "python"

jwt = JWTManager(app)


@app.route("/health")
def view_health():
    return {
        "v": 9
    }


@app.route("/login", methods=["POST"])
def view_login():
    access_token = create_access_token(identity = "cristhian")
    return {
        "access_token": access_token
    }


@app.route("/private")
@jwt_required()
def view_private():
    user_logged = get_jwt_identity()
    return {
        "user_logged": user_logged,
        "data": "PRIVATE-DATA"
    }