from flask_restful import reqparse, Resource
from models import Lesson

class LessonCreateAPI(Resource):
    def get(self):
        return [lesson.json() for lesson in Lesson.query.all()] 
    
    def post(self):
        _lesson_parser = reqparse.RequestParser()
        _lesson_parser.add_argument(
            "class_name", type=str, required=True, help="This field cannot be blank."
        )

        data = _lesson_parser.parse_args()
        _class = Lesson(**data)

        try:
            _class.save_to_db()
        except:
            return {'message': 'Error trying to make a class'}, 500

        return {'message': 'You have made a class!'}, 201