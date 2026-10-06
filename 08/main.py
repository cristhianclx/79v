from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from sqlalchemy.sql import func
from flask_restful import Resource, Api, reqparse


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)
ma = Marshmallow(app)


pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument('page', type=int, default=1, help='Page number')
pagination_parser.add_argument('per_page', type=int, default=10, help='Items per page')


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


class JokeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Joke
        load_instance = True
        datetimeformat = "%Y-%m-%d %H:%M:%S"


joke_schema = JokeSchema()
jokes_schema = JokeSchema(many = True)


class HealthResource(Resource):
    def get(self):
        return {
            'v': '8',
        }


class JokesResource(Resource):
    def get(self):
        #pagination_parameters = pagination_parser.parse_args()
        #page = pagination_parameters["page"]
        #per_page = pagination_parameters["per_page"]
        #data = Joke.query.paginate(page=page, per_page=per_page, error_out=False)
        #return jsonify({
        #    "metadata": {
        #        "page": data.page,
        #        "per_page": data.per_page,
        #        "total_items": data.total,
        #        "total_pages": data.pages,
        #        "has_next": data.has_next,
        #        "has_prev": data.has_prev,
        #    },
        #    "items": jokes_schema.dump(data.items),
        #})
        items = Joke.query.all()
        return jokes_schema.dump(items)

    def post(self):
        data = request.get_json()
        item = Joke(**data)
        db.session.add(item)
        db.session.commit()
        return joke_schema.dump(item), 201


class JokesIDResource(Resource):
    def get(self, id):
        item = Joke.query.get_or_404(id)
        return joke_schema.dump(item)

    def patch(self, id):
        item = Joke.query.get_or_404(id)
        data = request.get_json()
        joke_schema.load(
            data,
            instance=item,
            partial=True
        )
        db.session.commit()
        return joke_schema.dump(item)

    def delete(self, id):
        item = Joke.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {}, 204


api.add_resource(HealthResource, "/")
api.add_resource(JokesResource, "/jokes")
api.add_resource(JokesIDResource, "/jokes/<int:id>")