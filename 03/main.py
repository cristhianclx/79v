from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

db.init_app(app)


class Student(db.Model):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key = True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    language: Mapped[str]
    age: Mapped[int]
    city: Mapped[str]

    def __repr__(self):
        return "<Student: {}>".format(self.id)


class Teacher(db.Model):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(primary_key = True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    city: Mapped[str]
    age: Mapped[int]

    def __repr__(self):
        return "<Teacher: {}>".format(self.id)


@app.route("/")
def view_root():
    return {}


@app.route("/health")
def view_health():
    return {
        "status": "ok",
        "v": 3
    }


with app.app_context():
    db.create_all()
