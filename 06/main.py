from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from sqlalchemy.sql import func
from flask_restful import Resource, Api


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

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
users_schema = UserSchema(many = True)


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
messages_schema = MessageSchema(many = True)


class HealthResource(Resource):
    def get(self):
        return {'v': '6'}


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


class UsersByIDResource(Resource):
    def get(self, id):
        item = User.query.get_or_404(id)
        return user_schema.dump(item)

    def patch(self, id):
        item = User.query.get_or_404(id)
        data = request.get_json()
        user_schema.load(
            data,
            instance=item,
            partial=True
        )
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


class MessagesByIDResource(Resource):
    def get(self, id):
        item = Message.query.get_or_404(id)
        return message_schema.dump(item)


api.add_resource(HealthResource, '/')
api.add_resource(UsersResource, '/users')
api.add_resource(UsersByIDResource, '/users/<int:id>')
api.add_resource(MessagesResource, '/messages')
api.add_resource(MessagesByIDResource, '/messages/<int:id>')


# LABORATORIO
# /messages/ POST
# /messages/id/ PATCH
# /messages/id/ DELETE

# pantallazos: postman / insomnia / curl