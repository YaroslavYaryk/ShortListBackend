#!/usr/bin/env python
from app.main.database.db import initialize_db
import datetime
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from app.main.controller.api_auth import *
from app.main.model.models import *

# from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "92b5c7b10ed09879ca40ac46b236cdfb"

app.config["MONGODB_SETTINGS"] = "mongodb://localhost/prodaction_db"
app.permanent_session_lifetime = datetime.timedelta(minutes=20)
app.config.from_object(__name__)

initialize_db(app)

jwt = JWTManager(app)
api = Api(app)

app.register_blueprint(auth_api, url_prefix="/api/auth/")


@app.route("/")
def index():
    print(User.objects.all())
    return {"choice": True}


@jwt.expired_token_loader
def expired_token_callback():
    return (
        jsonify({"description": "The token has expired.", "error": "token_expired"}),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback():
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "unauthorization_required",
            }
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback():
    return (
        jsonify(
            {"description": "Signature veryfication failed.", "error": "invalid_token"}
        ),
        401,
    )


@jwt.revoked_token_loader
def revoked_token_callback():
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoke"}
        ),
        401,
    )


if __name__ == "__main__":
    app.run(debug=True)
