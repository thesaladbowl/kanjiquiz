from flask_restful import reqparse, Resource, inputs
from flask_jwt_extended import jwt_required, get_jwt_claims
from models import User, Student, Quiz, Lesson

from datetime import datetime

class QuizCorrectAPI(Resource):
    def get(self, class_id):
        lesson = Lesson.query.filter_by(class_name=class_id).first()
        correct = 0
        incorrect = 0

        for student in lesson.students:
            correct += student.correct_quizes()[0]
            incorrect += student.correct_quizes()[1]
        
        total = correct + incorrect

        quiz_tally = {"correct": correct, "incorrect": incorrect, "total": total}
        return quiz_tally

class QuizCreateAPI(Resource):
    def get(self):
        return [quiz.json() for quiz in Quiz.query.all().limit(10)]

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
        _quiz_parser.add_argument(
            "question_correct", type=inputs.boolean, required=False, help="This field cannot be blank."
        )
        
        data = _quiz_parser.parse_args()
        quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()
        if quiz:
            quiz.sentence = data['sentence']
            quiz.corrected_sentence = data['corrected_sentence']
            quiz.question_correct = data['question_correct']
            quiz.date_submitted = datetime.today()
            quiz.save_to_db()
            return quiz.json(), 201
        return {'message': 'could not update quiz'}, 500

