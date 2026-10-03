from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from sqlalchemy.sql import func
from flask_restful import Resource, Api


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)
ma = Marshmallow(app)


class Joke(db.Model):
    __tablename__ = "jokes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    routine_id = db.Column(db.Integer, nullable=True)
    show_id = db.Column(db.Integer, nullable=True)
    event_name = db.Column(db.String(255), nullable=True)
    show_name = db.Column(db.String(255), nullable=True)
    start_timestamp = db.Column(db.String(8), nullable=True)
    text = db.Column(db.Text)
    video_id = db.Column(db.String(20))

    def __repr__(self):
        return "<Joke: {}>".format(self.id)


class HealthResource(Resource):
    def get(self):
        return {
            'v': '8',
        }


api.add_resource(HealthResource, "/")


# crear la base de datos, migrar, aplicar migracion
# correr la shell, cargar los datos

# REST API
# /jokes
#   GET, POST
# /jokes/id
#   GET, PATCH, DELETE