from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/data")
def data():
    return "<p>data</p>"

@app.route("/ping")
def ping():
    return {
        "v": 1
    }

@app.route("/students")
def students():
    return [{
        "id": 1,
        "name": "A"
    }, {
        "id": 2,
        "name": "B"
    }]

@app.route("/students/<int:id_student>")
def get_student_by_id(id_student):
    return {
        "id": id_student,
        "name": "X",
        "courses": [{
            "id": "AB",
            "description": "Math"
        }, {
            "id": "AC",
            "description": "English"
        }]
    }

@app.route("/students/<int:id_student>/courses")
def get_student_courses_by_id(id_student):
    return [{
        "id": "AB",
        "description": "Math"
    }, {
        "id": "AC",
        "description": "English"
    }]

@app.route("/students/<int:id_student>/courses/<id_course>")
def get_course_student_courses_by_id(id_student, id_course):
    return {
        "id": id_course,
        "description": "Math"
    }