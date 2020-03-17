from db import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    user_type = db.Column(db.String(50))
    is_teacher = db.Column(db.Boolean)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity':'users',
        'polymorphic_on':type
    }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<User: {}>".format(self.username)

class Lesson(db.Model):

    class_id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50))
    students = db.relationship('Student', backref='class_name', lazy=True)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(class_name=_id).first()

    @classmethod 
    def find_by_name(cls, name):
        return cls.query.filter_by(class_name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            'class_id': self.class_id,
            'class_name': self.class_name,
            'students': [student.json() for student in self.students]
        }

    def __repr__(self):
        return "<Class: {}>".format(self.class_name)

class Student(User):
    __tablename__ = "students"

    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    lesson = db.Column(db.String, db.ForeignKey('lesson.class_name'))
    quizes = db.relationship('Quiz', backref='username', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity':'students',
    }

    def correct_quizes(self):
        total_correct = 0
        total_incorrect = 0

        for quiz in self.quizes:
            if quiz.question_correct:
                total_correct += 1
            else:
                total_incorrect += 1

        total = [total_correct, total_incorrect]
        
        return total

    def json(self):
        return {
            "full_name": f"{self.first_name} {self.last_name}",
            "id": self.student_id,
            "quizes": [quiz.json() for quiz in self.quizes]
        }

class Teacher(User):
    __tablename__ = "teachers"

    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    class_name = db.Column(db.String(10), db.ForeignKey('lesson.class_name'))

    __mapper_args__ = {
        'polymorphic_identity':'teachers',
    }

    def json(self):
        return {
            "first_name": self.first_name,
            "id": self.teacher_id,
            "is_teacher": self.is_teacher,
            "class_id": self.class_name
        }

class Quiz(db.Model):
    __tablename__ = "quiz_questions"

    quiz_id = db.Column(db.Integer, primary_key=True)
    quiz_name = db.Column(db.String(100))
    kanji = db.Column(db.String(50))
    sentence = db.Column(db.String(100))
    corrected_sentence = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    question_correct = db.Column(db.Boolean, default=False)
    student = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    comments = db.relationship("Comment")

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(quiz_name=name).first()
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Quiz: {}>".format(self.quiz_id)

    def json(self):
        return {
            "id": self.quiz_id,
            "quiz": self.quiz_name,
            "kanji": self.kanji,
            "sentence": self.sentence,
            "corrected_sentence": self.corrected_sentence,
            "question_correct": self.question_correct,
            "date_created": self.date_created.strftime("%B %d, %Y, %H:%M"),
            "date_submitted": self.date_submitted.strftime("%B %d, %Y, %H:%M")
        }

class Comment(db.Model):
    __tablename__ = "quiz_comments"

    id = db.Column(db.Integer, primary_key=True)
    quiz_comment_id = db.Column(db.Integer, db.ForeignKey('quiz_questions.quiz_id'))
    author = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comment = db.Column(db.Text, nullable=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            "comment": self.comment,
            "author": self.author,
            "id": self.id,
        }

    def __repr__(self):
        return "<Comment: {}>".format(self.quiz_comment_id)