from db import db
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
        return cls.query.filter_by(class_id=_id).first()

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
    lesson = db.Column(db.Integer, db.ForeignKey('lesson.class_id'))
    quizes = db.relationship('Quiz', backref='username', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity':'students',
    }

    def json(self):
        return {
            "first_name": self.first_name,
            "id": self.student_id,
            "quizes": [quiz.json() for quiz in self.quizes]
        }

class Teacher(User):
    __tablename__ = "teachers"

    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'teachers',
    }

    def json(self):
        return {
            "first_name": self.first_name,
            "id": self.student_id,
            "is_teacher": self.is_teacher,
        }

class Quiz(db.Model):
    __tablename__ = "quiz_questions"

    quiz_id = db.Column(db.Integer, primary_key=True)
    quiz_name = db.Column(db.String(100))
    kanji = db.Column(db.String(50))
    sentence = db.Column(db.String(100))
    student = db.Column(db.Integer, db.ForeignKey('students.student_id'))

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
            "quiz": self.quiz_name,
            "kanji": self.kanji,
            "sentence": self.sentence,
        }
