from flask_restful import Resource
from flask import jsonify, request, make_response, session
from app.main.model.models import *
import time
from functools import wraps
import datetime
from flask import Blueprint
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    decode_token,
)

auth_api = Blueprint("auth_api", __name__)


def get_access_token(email):
    user = User.objects.filter(Email=email).first()
    access_token = create_access_token(
        identity=user.get_id_str(), expires_delta=datetime.timedelta(minutes=40)
    )
    return user, access_token


def get_refresh_token(email):
    user = User.objects.filter(Email=email).first()
    refresh_token = create_refresh_token(
        identity=user.get_id_str(), expires_delta=datetime.timedelta(days=40)
    )
    return user, refresh_token


@auth_api.route("/token/refresh", methods=["POST"])
@jwt_required
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(
        identity=identity, expires_delta=datetime.timedelta(minutes=40)
    )

    return jsonify({"access": access})


def check_jwt_token(token):
    from run import app

    with app.app_context():
        # user, token = get_access_token("duhanov2003@gmail.com")
        data = decode_token(token)

        if data["exp"] - time.time():
            return True if User.objects.filter(id=data["identity"]) else False
        return False


def manipulate_user_tockens():
    from run import app

    with app.app_context():

        print(get_access_token("duhanov2003@gmail.com")[1])

        for elem in Tokens.objects.all():
            # print(elem.activationToken)
            if not check_jwt_token(elem.activationToken):
                elem.delete()


def check_all_tokens(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "token_ckeck" not in session:
            manipulate_user_tockens()
            session["token_ckeck"] = True

        return f(current_user, *args, **kwargs)

    return decorated
