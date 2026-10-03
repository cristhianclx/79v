from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from sqlalchemy.sql import func
from flask_restful_swagger_3 import Api, Resource, swagger, Schema


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)
ma = Marshmallow(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(11), nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<User: {}>".format(self.id)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        datetimeformat = "%Y-%m-%d %H:%M:%S"


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserSimpleSchema(ma.SQLAlchemySchema):
    first_name = ma.auto_field()
    last_name = ma.auto_field()

    class Meta:
        model = User
        datetimeformat = "%Y-%m-%d %H:%M:%S"


user_simple_schema = UserSimpleSchema()
users_simple_schema = UserSimpleSchema(many=True)


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref="user")

    def __repr__(self):
        return "<Message: {}>".format(self.id)


class MessageSchema(ma.SQLAlchemyAutoSchema):
    user = ma.Nested(UserSchema)

    class Meta:
        model = Message
        load_instance = True
        include_fk = True
        datetimeformat = "%Y-%m-%d %H:%M:%S"


message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)


class MessageSimpleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        load_instance = True
        datetimeformat = "%Y-%m-%d %H:%M:%S"


message_simple_schema = MessageSimpleSchema()
messages_simple_schema = MessageSimpleSchema(many=True)


class HealthResource(Resource):
    def get(self):
        return {"v": "6"}


class UsersResource(Resource):
    def get(self):
        items = User.query.all()
        return users_schema.dump(items)

    def post(self):
        data = request.get_json()
        item = User(**data)
        db.session.add(item)
        db.session.commit()
        return user_schema.dump(item), 201


class UsersPublicResource(Resource):
    def get(self):
        items = User.query.all()
        return users_simple_schema.dump(items)


class UsersByIDResource(Resource):
    def get(self, id):
        item = User.query.get_or_404(id)
        return user_schema.dump(item)

    def patch(self, id):
        item = User.query.get_or_404(id)
        data = request.get_json()
        user_schema.load(data, instance=item, partial=True)
        db.session.commit()
        return user_schema.dump(item)

    def delete(self, id):
        item = User.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {}, 204


class MessagesResource(Resource):
    def get(self):
        items = Message.query.all()
        return messages_schema.dump(items)

    def post(self):
        data = request.get_json()
        item = Message(**data)
        db.session.add(item)
        db.session.commit()
        return message_schema.dump(item), 201


class MessagesByIDResource(Resource):
    def get(self, id):
        item = Message.query.get_or_404(id)
        return message_schema.dump(item)

    def patch(self, id):
        item = Message.query.get_or_404(id)
        data = request.get_json()
        message_schema.load(data, instance=item, partial=True)
        db.session.commit()
        return message_schema.dump(item)

    def delete(self, id):
        item = Message.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {}, 204


class UsersByIDMessagesResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        items = Message.query.filter_by(user=user).all()
        return messages_simple_schema.dump(items)

    def post(self, user_id):
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        item = Message(**data)
        item.user = user
        db.session.add(item)
        db.session.commit()
        return message_simple_schema.dump(item), 201


api.add_resource(HealthResource, "/")
api.add_resource(UsersResource, "/users")
api.add_resource(UsersPublicResource, "/users/public")
api.add_resource(UsersByIDResource, "/users/<int:id>")
api.add_resource(MessagesResource, "/messages")
api.add_resource(MessagesByIDResource, "/messages/<int:id>")
api.add_resource(UsersByIDMessagesResource, "/users/<int:user_id>/messages")


class EmailModel(Schema):
    type = "string"
    format = "email"


class KeysModel(Schema):
    type = "object"
    properties = {"name": {"type": "string"}}


class UserModel(Schema):
    properties = {
        "id": {
            "type": "integer",
            "format": "int64",
        },
        "name": {"type": "string"},
        "mail": EmailModel,
        "keys": KeysModel.array(),
        "user_type": {"type": "string", "enum": ["admin", "regular"], "nullable": True},
        "password": {"type": "string", "format": "password", "load_only": True},
    }
    required = ["name"]


class UserItemResource(Resource):
    @swagger.tags(["user"])
    @swagger.reorder_with(UserModel, description="Returns a user", summary="Get User")
    def get(self, user_id):
        # Do some processing
        return (
            UserModel(**{"id": 1, "name": "somebody"}),
            200,
        )  # generates json response {"id": 1, "name": "somebody"}


api.add_resource(UserItemResource, "/api/users/<int:user_id>")
