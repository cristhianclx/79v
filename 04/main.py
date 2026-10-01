from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


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


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref="user")
    
    def __repr__(self):
        return "<Message: {}>".format(self.id)


@app.route("/")
def view_root():
    return {}


@app.route("/health")
def view_health():
    return {
        "status": "ok",
        "v": 4
    }


@app.route("/users")
def view_users():
    items = User.query.all()
    return render_template("users.html", items=items)


@app.route("/users/add", methods=["GET", "POST"])
def view_users_add():
    if request.method == "GET":
        return render_template("users-add.html")
    if request.method == "POST":
        item = User(
            code=request.form["code"],
            first_name=request.form["first_name"],
            last_name=request.form["last_name"],
            age=request.form["age"],
        )
        db.session.add(item)
        db.session.commit()
        return render_template("users-add.html", message="User saved")


@app.route("/users/<int:user_id>")
def view_users_by_id(user_id):
    item = User.query.get_or_404(user_id)
    return render_template("users-view.html", item=item)


@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
def view_users_edit_by_id(user_id):
    item = User.query.get_or_404(user_id)
    if request.method == "GET":
        return render_template("users-edit.html", item=item)
    if request.method == "POST":
        item.code = request.form["code"]
        item.first_name=request.form["first_name"]
        item.last_name=request.form["last_name"]
        item.age=request.form["age"]
        db.session.add(item)
        db.session.commit()
        return render_template("users-edit.html", item=item, message="User saved")


@app.route("/users/<int:user_id>/delete", methods=["GET", "POST"])
def view_users_delete_by_id(user_id):
    item = User.query.get_or_404(user_id)
    if request.method == "GET":
        return render_template("users-delete.html", item=item)
    if request.method == "POST":
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('view_users'))


@app.route("/users/<int:user_id>/messages")
def view_messages_by_user_id(user_id):
    user = User.query.get_or_404(user_id)
    items = Message.query.filter_by(user=user).all()
    return render_template("messages.html", items=items)


@app.route("/messages")
def view_messages():
    items = Message.query.all()
    return render_template("messages.html", items=items)


@app.route("/messages/add", methods=["GET", "POST"])
def view_messages_add():
    users = User.query.all()
    if request.method == "GET":
        return render_template("messages-add.html", users=users)
    if request.method == "POST":
        item = Message(
            content=request.form["content"],
            user_id=request.form["user_id"],
        )
        db.session.add(item)
        db.session.commit()
        return render_template("messages-add.html", users=users, message="Message saved")


@app.route("/messages/<int:message_id>")
def view_messages_by_id(message_id):
    item = Message.query.get_or_404(message_id)
    return render_template("messages-view.html", item=item)


@app.route("/messages/<int:message_id>/edit", methods=["GET", "POST"])
def view_messages_edit_by_id(message_id):
    item = Message.query.get_or_404(message_id)
    if request.method == "GET":
        return render_template("messages-edit.html", item=item)
    if request.method == "POST":
        item.content = request.form["content"]
        item.user_id = request.form["user_id"]
        db.session.add(item)
        db.session.commit()
        return render_template("messages-edit.html", item=item, message="Message saved")


@app.route("/messages/<int:message_id>/delete", methods=["GET", "POST"])
def view_messages_delete_by_id(message_id):
    item = Message.query.get_or_404(message_id)
    if request.method == "GET":
        return render_template("messages-delete.html", item=item)
    if request.method == "POST":
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('view_messages'))