from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Faculty(db.Model):
    __tablename__ = 'faculty'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), index=True, unique=True)
    groups = db.relationship('Group', lazy='dynamic')

    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return '<Faculty {}>'.format(self.name)

class Edgroup(db.Model):
    __tablename__ = 'edgroup'
    
    id = db.Column(db.String(10), primary_key=True)
    course = db.Column(db.Integer)
    faculty = db.Column(db.Integer, db.ForeignKey('faculty.id'))

    def __init__(self, course, faculty):
        self.course = course
        self.faculty = faculty
    def __repr__(self):
        return '<Edgroup {}, faculty {}>'.format(self.course, self.faculty)

class Subject(db.Model):
    __tablename__ = 'subject'

    name = db.Column(db.String(100), primary_key=True)

    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f""

class AssignedClass(db.Model):
    __tablename__ = 'assignedclass'

    edgroup = db.Column(db.String(10), db.ForeignKey('edgroup.id'), primary_key=True)
    subject = db.Column(db.String(100), db.ForeignKey('subject.name'), primary_key=True)

    def __init__(self, edgroup, subject):
        self.edgroup = edgroup                  
        self.subject = subject                     
    def __repr__(self):
        return f""

class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    grants = db.Column(db.Integer)
    education = db.Column(db.String(50))
    edgroup = db.Column(db.String(10), db.ForeignKey('edgroup.id'))

    def __init__(self, id, name, grants,education, edgroup):
        self.id = id
        self.name = name
        self.grants = grants
        self.education = education
        self.edgroup = edgroup
    def __repr__(self):
        return f""

class Test(db.Model):
    __tablename__ = 'test'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    subject = db.Column(db.String(100), db.ForeignKey('subject.name'), primary_key=True, unique=True) 
    db.relationship('TestDeadline', lazy='dynamic')

    def __init__(self, id, subject):
        self.id = id
        self.subject = subject
    def __repr__(self):
        return f""

class Labwork(db.Model):
    __tablename__ = 'labwork'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    subject = db.Column(db.String(100), db.ForeignKey('subject.name'), primary_key=True, unique=True)

    def __init__(self, id, subject):
        self.id = id
        self.subject = subject
    def __repr__(self):
        return f""

class TestDeadline(db.Model):
    __tablename__ = 'testdeadline'

    id = db.Column(db.Integer, db.ForeignKey('test.id'), primary_key=True)      
    subject = db.Column(db.String(50), db.ForeignKey('test.subject'), primary_key=True)
    edgroup = db.Column(db.String(10), db.ForeignKey('edgroup.id'), primary_key=True)
    deadline = db.Column(db.DateTime)

    '''__table_args__ = (
        db.ForeignKeyConstraint(['id'], ['test.id'], name='fk_testdl_test_id'),
        db.ForeignKeyConstraint(['subject'], ['test.subject'], name='fk_testdl_test_subj')
    )'''

    def __init__(self, id, subject, edgroup):
        self.id = id
        self.subject = subject
        self.edgroup = edgroup
    def __repr__(self):
        return f""


class TestPass(db.Model):
    __tablename__ = 'testpass'
    id = db.Column(db.Integer, db.ForeignKey('test.id'), primary_key=True)
    studentid = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    subject = db.Column(db.String(50), db.ForeignKey('test.subject'), primary_key=True)

    '''__table_args__ = (
        db.ForeignKeyConstraint(['id'], ['test.id'], name='fk_testpass_test_id'),
        db.ForeignKeyConstraint(['subject'], ['test.subject'], name='fk_testpass_test_subj')
    )'''

    def __init__(self, id, studentid, subject):
        self.id = id
        self.studentid = studentid
        self.subject = subject
    def __repr__(self):
        return f""

class LabworkPass(db.Model):
    __tablename__ = 'labworkpass'

    id = db.Column(db.Integer, db.ForeignKey('labwork.id'), primary_key=True)
    subject = db.Column(db.String(50), db.ForeignKey('labwork.subject'), primary_key=True)
    studentid = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    mark = db.Column(db.Integer)

    def __init__(self, id, subject, studentid, mark):
        self.id = id
        self.studentid = studentid
        self.subject = subject
        self.mark = mark
    def __repr__(self):
        return f""


class LabworkDeadline(db.Model):
    __tablename__ = 'labworkdeadline'

    id = db.Column(db.Integer, db.ForeignKey('labwork.id'), primary_key=True)
    subject = db.Column(db.String(100), db.ForeignKey('labwork.subject'), primary_key=True)
    edgroupId = db.Column(db.String(10), db.ForeignKey('edgroup.id'), primary_key=True)
    deadline = db.Column(db.DateTime)

    def __init__(self, id, subject, edgroupId, deadline):
        self.id = id
        self.subject = subject
        self.edgroupId = edgroupId
        self.deadline = deadline

    def __repr__(self):
        return f""

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(50), unique=True)
    hash = db.Column(db.String(256), unique=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
