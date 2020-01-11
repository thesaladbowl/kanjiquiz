from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import User
from resources.users import StudentList, StudentRegister, UserLogin, UserDelete, TeacherRegister, StudentRetrieveAPI
from resources.quiz import QuizCreateAPI, QuizDeleteAPI, QuizReadUpdateAPI
from resources.lesson import LessonCreateAPI

from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "salaidisdelicious"

@app.before_first_request
def create_tables():
    db.create_all()

api = Api(app)
jwt = JWTManager(app)
cors = CORS(app, expose_headers='Authorization')

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user = User.find_by_id(identity)
    if user.is_teacher:
        return {'authorized': True}
    
api.add_resource(StudentList, "/students")
api.add_resource(StudentRetrieveAPI, "/students/<int:student_id>")
api.add_resource(StudentRegister, "/students/register")
api.add_resource(TeacherRegister, "/teachers/register")

api.add_resource(QuizReadUpdateAPI, "/quiz/<int:quiz_id>")
api.add_resource(QuizCreateAPI, "/quiz")
api.add_resource(QuizDeleteAPI, "/quiz/delete/<int:quiz_id>") 

api.add_resource(LessonCreateAPI, "/lesson")

api.add_resource(UserLogin, "/login")
api.add_resource(UserDelete, "/user/delete/<int:user_id>")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
