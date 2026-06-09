from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Training(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sport_type = db.Column(db.String(50), nullable=False)  # run, swim, gym
    duration = db.Column(db.Integer, nullable=False)  # минуты
    distance = db.Column(db.Float, nullable=True)  # километры
    intensity = db.Column(db.Integer, nullable=True)  # 1-10
    calories = db.Column(db.Integer, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'sport_type': self.sport_type,
            'duration': self.duration,
            'distance': self.distance,
            'intensity': self.intensity,
            'calories': self.calories,
            'date': self.date.strftime('%Y-%m-%d')
        }