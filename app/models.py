from app import db

class Faculty(db.Model):
    __tablename__ = 'faculty'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

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

    name = db.Column(db.Integer, primary_key=True)

    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f""

class AssignedClass(db.Model):
    __tablename__ = 'assignedclass'

    edgroup = db.Column(db.Integer, db.ForeignKey('edgroup.id'), primary_key=True)
    subject = db.Column(db.Integer, db.ForeignKey('subject.name'), primary_key=True)

    def __init__(self, edgroup, subject):
        self.edgroup = edgroup                  
        self.subject = subject                     
    def __repr__(self):
        return f""

class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    grants = db.Column(db.Integer)
    education = db.Column(db.String())
    edgroup = db.Column(db.String(10), db.ForeignKey('edgroup.id'))

    def __init__(self, id, name, grants,education, edgroup):
        self.id = id
        self.name = name
        self.grants = grants
        self.education = education
        self.edgroup = edgroup
    def __repr__(self):
        return f""

class Labwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String()), db.ForeignKey('subject.name', primary_key=True)

    def __init__(self, id, subject):
        self.id = id
        self.subject = subject
    def __repr__(self):
        return f""

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(), db.ForeignKey('subject.name'), primary_key=True)  

    def __init__(self, id, subject):
        self.id = id
        self.subject = subject
    def __repr__(self):
        return f""

class TestDeadline(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('test.id'), primary_key=True)      
    subject = db.Column(db.String(), db.ForeignKey('test.subject'), primary_key=True)
    edgroup = db.Column(db.String(), primary_key=True)
    deadline = db.Column(db.DateTime)

    def __init__(self, id, subject, edgroup):
        self.id = id
        self.subject = subject
        self.edgroup = edgroup
    def __repr__(self):
        return f""

class TestPass(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('test.id'), primary_key=True)
    studentid = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    subject = db.Column(db.String(), db.ForeignKey('test.subject'), primary_key=True)

    def __init__(self, id, studentid, subject):
        self.id = id
        self.studentid = studentid
        self.subject = subject
    def __repr__(self):
        return f""

class LabworkPass(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('labwork.id'), primary_key=True)
    subject = db.Column(db.String(), db.ForeignKey('labwork.subject'), primary_key=True)
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
    id = db.Column(db.Integer, db.ForeignKey('labwork.id'), primary_key=True)
    subject = db.Column(db.String(), db.ForeignKey('labwork.subject'), primary_key=True)
    edgroupId = db.Column(db.Integer, db.ForeignKey('edgroup.id'), primary_key=True)
    deadline = db.Column(db.DateTime)

    def __init__(self, id, subject, edgroupId, deadline):
        self.id = id
        self.subject = subject
        self.edgroupId = edgroupId
        self.deadline = deadline
    def __repr__(self):
        return f""

    
