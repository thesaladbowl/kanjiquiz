from flask import Flask, redirect, url_for, render_template, request
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import Quiz, Lesson, Student, Teacher
from resources.users import StudentList, StudentRegister, UserLogin, UserDelete, TeacherRegister, StudentRetrieveAPI, TeacherInfo, TokenRefresh
from resources.quiz import QuizCreateAPI, QuizDeleteAPI, QuizReadUpdateAPI, QuizCorrectAPI
from resources.comment import CommentCreateAPI, CommentRetreieveAPI
from resources.lesson import LessonCreateAPI

from db import db
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user
from forms import LoginForm

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
login = LoginManager(app)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "salaidisdelicious"

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Quiz': Quiz}

@app.before_first_request
def create_tables():
    db.create_all()

api = Api(app)
jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user = User.find_by_id(identity)
    if user.is_teacher:
        return {'authorized': True}
    
api.add_resource(StudentList, "/student_list/<string:class_id>")
api.add_resource(StudentRetrieveAPI, "/students/<int:student_id>")
api.add_resource(StudentRegister, "/students/register")
api.add_resource(TeacherRegister, "/teachers/register")
api.add_resource(TeacherInfo, "/teacher/<int:teacher_id>")

api.add_resource(QuizReadUpdateAPI, "/quiz/<int:quiz_id>")
api.add_resource(QuizCreateAPI, "/quiz")
api.add_resource(QuizDeleteAPI, "/quiz/delete/<int:quiz_id>") 

api.add_resource(CommentCreateAPI, "/comment/create")
api.add_resource(CommentRetreieveAPI, "/comment/<int:quiz_id>")

api.add_resource(LessonCreateAPI, "/lesson")

api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserDelete, "/user/delete/<int:user_id>")

api.add_resource(QuizCorrectAPI, "/stats/<string:class_id>/qcorrect")

# Admin Login, Views

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_teacher

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))
        
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_teacher

admin = Admin(app, name="KanjiQuiz", index_view=MyAdminIndexView())
admin.add_view(MyModelView(Quiz, db.session))
admin.add_view(MyModelView(Student, db.session))
admin.add_view(MyModelView(Teacher, db.session))

admin.add_view(MyModelView(Lesson, db.session))

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            print('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('admin.index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/admin/logout')
def logout():
    logout_user()
    return 'Logged Out!'

@app.route('/')
def index():
    return render_template("index.html")

db.init_app(app)
if __name__ == "__main__":
    app.run(port=5000, debug=True)
