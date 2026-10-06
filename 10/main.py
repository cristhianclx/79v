from flask import Flask, render_template
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


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    nickname = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Message {self.id}>"


class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        load_instance = True
        datetimeformat = "%Y-%m-%d %H:%M:%S"


message_schema = MessageSchema()


@app.route("/")
def view_index():
    return render_template("index.html")


@app.route("/room")
def view_room():
    items = Message.query.all()
    return render_template("room.html", items=items)


@socketio.on("ws-welcome")
def handle_ws_welcome(data, methods=["GET", "POST"]):
    print("received: " + str(data))


@socketio.on("ws-messages")
def handle_ws_messages(data, methods=["GET", "POST"]):
    item = Message(**data)
    db.session.add(item)
    db.session.commit()
    socketio.emit("ws-messages-responses", message_schema.dump(item))


# crear una tabla Room
# en la tabla Message, crearle el Room como FK
# en el index.html y en la vista view_index, mostrar todas las salas
# crear la opcion de crear una sala nueva (id, created, name, max_messages)
# max_messages, numero maximo de mensajes para enviar en una sala
# en la vista de room, mostrar solo los mensajes de una sala
# en los mensajes agrega un campo importance (high, normal)
# si es high que al mostrar el mensaje salga en rojo