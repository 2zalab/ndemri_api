import json

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):

    username = db.Column(db.String, primary_key=True)
    authenticated = db.Column(db.Boolean, default=False)

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated


class Soil(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    longitude = db.Column(db.String)
    latitude = db.Column(db.String)
    timestamp = db.Column(db.String, nullable=False)
    temperature = db.Column(db.String)
    humidity = db.Column(db.String)
    predictions = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return json.dumps(
            {
                'id': self.id,
                'user_id': self.user_id,
                'image_url': self.image_url,
                'name': self.name,
                'longitude': self.longitude,
                'latitude': self.latitude,
                'timestamp': self.timestamp,
                'temperature': self.temperature,
                'humidity': self.humidity,
                'predictions': self.predictions,
            }
        )
