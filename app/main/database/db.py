from mongoengine import connect
from app.main.model.models import *
from app.main.database.default_db_data import OCCUPATION, CATEGORY_TO_BD


def initialize_db(app):
    connect(host=app.config["MONGODB_SETTINGS"])

    if not len(Category.objects.all()) and len(Occupation.objects.all()):  # empty tables

        for category_name in CATEGORY_TO_BD:
            Category(
                Name=category_name["name"], english_name=category_name["english_name"]
            ).save()

        for occupation_name in OCCUPATION:
            Occupation(
                Name=occupation_name["name"],
                english_name=occupation_name["english_name"],
            ).save()
