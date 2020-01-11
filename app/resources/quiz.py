from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required, get_jwt_claims
from models import User, Student, Quiz, Lesson

class QuizCreateAPI(Resource):
    def get(self):
        return [quiz.json() for quiz in Quiz.query.all()]

    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        _quiz_parser = reqparse.RequestParser()
        _quiz_parser.add_argument(
            "kanji", type=str, required=True, help="This field cannot be blank."
        )
        _quiz_parser.add_argument(
            "sentence", type=str, required=True, help="This field cannot be blank."
        )
        _quiz_parser.add_argument(
            "quiz_name", type=str, required=True, help="This field cannot be blank."
        )
        _quiz_parser.add_argument(
            "class_name", type=str, required=True, help="This field cannot be blank."
        )

        data = _quiz_parser.parse_args()
        _class = Lesson.find_by_name(data['class_name'])
        student_list = [student for student in _class.students]

        try:
            if claims['authorized']:
                for student in student_list:
                    q = Quiz(kanji=data['kanji'], sentence=data['sentence'], quiz_name=data['quiz_name'], username=student)
                    q.save_to_db()
        except Exception as e:
            print(e)
            return {'message': 'Quiz could not be created'}, 500

        return {'message': 'quiz created!'}, 201

class QuizDeleteAPI(Resource): # Deletes ALL quiz entries, not a single one
    @jwt_required
    def delete(self, quiz_id):
        claims = get_jwt_claims()
        quiz_list = Quiz.query.filter_by(quiz_id=quiz_id)
        if quiz_list and claims['authorized']:
            for quiz in quiz_list:
                quiz.delete_from_db()
            return {'message': 'Quiz deleted!'}, 200
        return {'message': 'Quiz could not be found'}, 404

class QuizReadUpdateAPI(Resource): # Edits a single quiz, by ID. Can also retreieve a single quiz instance
    def get(self, quiz_id):
        quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()
        return quiz.json()

    @jwt_required
    def put(self, quiz_id):
        _quiz_parser = reqparse.RequestParser()
        _quiz_parser.add_argument(
            "sentence", type=str, required=True, help="This field cannot be blank."
        )
        _quiz_parser.add_argument(
            "corrected_sentence", type=str, required=False, help="This field cannot be blank."
        )
        data = _quiz_parser.parse_args()
        quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()
        if quiz:
            quiz.sentence = data['sentence']
            quiz.corrected_sentence = data['corrected_sentence']
            quiz.save_to_db()
            return quiz.json(), 201
        return {'message': 'could not update quiz'}, 500


"""

 To do:
 1. ReadUpdateApi endpoint needs to be modified to read and edit a students quiz ie filter by quiz id AND student id 

"""
