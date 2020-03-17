from flask_restful import reqparse, Resource, inputs
from flask_jwt_extended import jwt_required
from models import User, Quiz, Comment

class CommentCreateAPI(Resource):
    @jwt_required
    def post(self):
        _comment_parser = reqparse.RequestParser()

        _comment_parser.add_argument(
            "comment", type=str, required=True, help="This field cannot be blank."
        )
        _comment_parser.add_argument(
            "user_id", type=int, required=True, help="This field cannot be blank."
        )
        _comment_parser.add_argument(
            "quiz_id", type=int, required=True, help="This field cannot be blank."
        )

        data = _comment_parser.parse_args()

        try:
            comment = Comment(quiz_comment_id=data['quiz_id'], author=data['user_id'], comment=data['comment'] )
        except Exception as e:
            print(e)
            return {'message': 'Comment could not be created'}, 500

        comment.save_to_db()

        return comment.json(), 201

class CommentRetreieveAPI(Resource):
    def get(self, quiz_id):
        return [comment.json() for comment in Comment.query.filter_by(quiz_comment_id=quiz_id).order_by(Comment.date_created.desc()).limit(10)]




