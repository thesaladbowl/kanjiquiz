from flask import jsonify
from flask_restful import reqparse, Resource
from models import User, Student, Lesson, Teacher
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_claims, jwt_required

class StudentRetrieveAPI(Resource):
    def get(self, student_id):
        return Student.find_by_id(student_id).json()

class StudentList(Resource):
    def get(self, class_id):
        student_list = Student.query.filter_by(lesson=class_id)
        return [student.json() for student in student_list]

class StudentRegister(Resource):
    def post(self):
        _user_parser = reqparse.RequestParser()
        _user_parser.add_argument(
            "username", type=str, required=True, help="This field cannot be blank."
        )
        _user_parser.add_argument(
            "password", type=str, required=True, help="This field cannot be blank."
        )
        _user_parser.add_argument(
            "first_name", type=str, required=True, help="This field cannot be blank."
        )
        _user_parser.add_argument(
            "last_name", type=str, required=True, help="This field cannot be blank."
        )
        _user_parser.add_argument(
            "is_teacher", type=bool, required=True, help="This field cannot be blank."
        )
        _user_parser.add_argument(
            "class_id", type=str, required=True, help="This field cannot be blank."
        )
        data = _user_parser.parse_args()
        _class = Lesson.find_by_name(data["class_id"]) # Need to add parser for ID and then pass this as the argument

        if User.find_by_username(data["username"]):
            return {'message': 'A user with that name already exists'}

        student = Student(username=data['username'],
                          first_name=data['first_name'],
                          last_name=data['last_name'],
                          is_teacher=data['is_teacher'],
                          class_name=_class)
        student.set_password(data['password'])
        student.save_to_db()

        return {"message": "Student Created!"}, 201

class TeacherInfo(Resource):
    def get(self, teacher_id):
        return Teacher.query.filter_by(teacher_id=teacher_id).first().json() 

class TeacherRegister(Resource):
    def post(self):
        _user_parser = reqparse.RequestParser()
        _user_parser.add_argument(
            "username", type=str, required=True, help="This field cannot be blank."
        )
        _user_parser.add_argument(
            "password", type=str, required=True, help="This field cannot be blank."
        )
        _user_parser.add_argument(
            "first_name", type=str, required=True, help="This field cannot be blank."
        )
        _user_parser.add_argument(
            "last_name", type=str, required=True, help="This field cannot be blank."
        )
        _user_parser.add_argument(
            "is_teacher", type=bool, required=True, help="This field cannot be blank."
        )
        _user_parser.add_argument(
            "class_name", type=str, required=True, help="This field cannot be blank."
        )
        data = _user_parser.parse_args()

        if User.find_by_username(data["username"]):
            return {'message': 'A user with that name already exists'}

        if not Lesson.find_by_name(data['class_name']):
            return  {'message': 'There is no class with that name'}

        teacher = Teacher(username=data['username'], first_name=data['first_name'], last_name=data['last_name'], is_teacher=data['is_teacher'], class_name=data['class_name'])
        teacher.set_password(data['password'])
        teacher.save_to_db()

        return {"message": "Teacher Created!"}, 201

class UserLogin(Resource):
    def post(self):
        _login_parser = reqparse.RequestParser()
        _login_parser.add_argument(
            "username", type=str, required=True, help="This field cannot be blank."
        )
        _login_parser.add_argument(
            "password", type=str, required=True, help="This field cannot be blank."
        )

        data = _login_parser.parse_args()
        user = User.find_by_username(data['username'])
        
        pw = data['password']
        class_id = None

        if user and pw:
            if user.check_password(pw):
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                if user.is_teacher:
                    class_id = user.class_name
                    
                return {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': user.is_teacher,
                    'class_id': class_id
                }, 200
            else:
                return {'message': 'Password is not correct'}, 400
        else:
            return {'message': 'Invalid Credentials'}, 400

class UserDelete(Resource):
    @jwt_required
    def delete(self, user_id):
        claims = get_jwt_claims()
        user = Student.find_by_id(user_id)
        if user and claims['authorized']:
            user.delete_from_db()
            return {'message': 'User deleted!'}, 200
        
        return {'message': 'User not found'}, 404

