import json

from flask_sqlalchemy import SQLAlchemy

from vendors.cache import store_soil
from vendors.db_models import Soil


def get_db(_app):
    return SQLAlchemy(_app)


def store_prediction_record(_app, id, file_path, prediction, data):

    prediction = json.dumps(prediction)

    soil = Soil(
        user_id=id,
        image_url=file_path,
        name=data.get('name'),
        timestamp=data.get('timestamp'),
        predictions=prediction,
    )

    store_soil(soil)


def add_record(_app, record):

    db = get_db(_app)
    db.session.add(record)
    db.session.commit()


def create_db(_app):
    db = get_db(_app)

    with _app.app_context():
        db.create_all()


def init_db(_app):
    db = get_db(_app)

    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///soil_care.db"
    db.init_app(_app)


def current_user():
    return None