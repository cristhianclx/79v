from flask import Flask, render_template, request
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
app.config['SECRET_KEY'] = 'python'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

ma = Marshmallow(app)

socketio = SocketIO(app)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    name = db.Column(db.Integer, nullable=False)
    messages_max = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Room {self.id}>"


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    nickname = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    importance = db.Column(db.String(150), nullable=False)

    room_id = db.Column(db.Integer, db.ForeignKey("room.id"))
    room = db.relationship("Room", backref="room")

    def __repr__(self):
        return f"<Message {self.id}>"


class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        load_instance = True
        include_fk = True
        datetimeformat = "%Y-%m-%d %H:%M:%S"


message_schema = MessageSchema()


@app.route("/")
def view_index():
    items = Room.query.all()
    return render_template("index.html", items=items)


@app.route("/rooms/add", methods=["GET", "POST"])
def view_rooms_add():
    if request.method == "GET":
        return render_template("rooms-add.html")
    if request.method == "POST":
        item = Room(
            name=request.form["name"],
            messages_max=request.form["messages_max"],
        )
        db.session.add(item)
        db.session.commit()
        return render_template("rooms-add.html", message="Room saved")



@app.route("/room/<id>")
def view_room_by_id(id):
    room = Room.query.get_or_404(id)
    items = Message.query.filter_by(room = room).all()
    return render_template("room.html", items=items, room=room)


@socketio.on("ws-welcome")
def handle_ws_welcome(data, methods=["GET", "POST"]):
    print("received: " + str(data))


@socketio.on("ws-messages")
def handle_ws_messages(data, methods=["GET", "POST"]):
    room = Room.query.get_or_404(data["room_id"])
    messages = Message.query.filter_by(room = room).count()
    if room.messages_max <= messages:
        socketio.emit("ws-messages-error-".format(room.id), {})
    else:
        item = Message(**data)
        db.session.add(item)
        db.session.commit()
        socketio.emit("ws-messages-responses", message_schema.dump(item))


# LABORATORIO
# max_messages, numero maximo de mensajes para enviar en una sala