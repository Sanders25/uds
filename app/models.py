from calendar import c
from app import db, adminManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_admin import BaseView, expose, AdminIndexView, Admin
from app import loginManager
from hashlib import md5
from flask_admin.contrib.sqla import ModelView

#region Table Models
class Faculty(db.Model):
    __tablename__ = 'faculty'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), index=True, unique=True)

    def __repr__(self):
        return '№ {} - инст. {}'.format(self.id, self.name)

class Edgroup(db.Model):
    __tablename__ = 'edgroup'
    
    id = db.Column(db.String(10), primary_key=True)
    course = db.Column(db.Integer)
    faculty = db.Column(db.Integer, db.ForeignKey('faculty.id'))

    faculties = db.relationship('Faculty')
    students = db.relationship('Student', lazy='dynamic')

    def __repr__(self):
        return '№ {}, инст. {}'.format(self.id, self.faculty)

class EdgroupView(ModelView):
    column_display_pk = True
    form_columns = ['id', 'faculties', 'course']

class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    grants = db.Column(db.Integer)
    education = db.Column(db.String(50))
    edgroup = db.Column(db.String(10), db.ForeignKey('edgroup.id'))
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))

    group = db.relationship("Edgroup", backref="student_groups")
    users = db.relationship("User")

    def __repr__(self):
        return 'Зач. {}, гр. {}'.format(self.id, self.edgroup)

class StudentView(ModelView):
    form_columns = ['name', 'group','users']

class Subject(db.Model):
    __tablename__ = 'subject'

    name = db.Column(db.String(100), primary_key=True)
    staffId = db.Column(db.Integer, db.ForeignKey('staff.id'))

    instructors = db.relationship("Staff")

    def __repr__(self):
        return '{}'.format(self.name)

class SubjectView(ModelView):
    column_display_pk = True
    form_columns = ['name', 'instructors']
    column_hide_backrefs = False

class AssignedClass(db.Model):
    __tablename__ = 'assignedclass'

    edgroup = db.Column(db.String(10), db.ForeignKey('edgroup.id'), primary_key=True)
    subject = db.Column(db.String(100), db.ForeignKey('subject.name'), primary_key=True)

    groups = db.relationship('Edgroup')
    subjects = db.relationship('Subject')
               
    def __repr__(self):
        return '№ гр. {}, {}'.format(self.edgroup, self.subject)

class AssignedClassView(ModelView):
    column_display_pk = True
    form_columns = ['groups', 'subjects']

class Test(db.Model):
    __tablename__ = 'test'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), db.ForeignKey('subject.name'), primary_key=True) 
    name = db.Column(db.String(100))

    subjects = db.relationship('Subject')

    def __repr__(self):
        return '№ {}:{} - {}'.format(self.id, self.subject, self.name)

class TestView(ModelView):
    column_display_pk = True
    form_columns = ['id', 'subjects', 'name']

class Labwork(db.Model):
    __tablename__ = 'labwork'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), db.ForeignKey('subject.name'), primary_key=True)
    name = db.Column(db.String(100))

    subjects = db.relationship('Subject')

    def __repr__(self):
        return '№ {}, {}'.format(self.id, self.subject)

class LabworkView(ModelView):
    column_display_pk = True
    form_columns = ['id', 'subjects', 'name']
    column_hide_backrefs = False

class TestDeadline(db.Model):
    __tablename__ = 'testdeadline'

    id = db.Column(db.Integer, primary_key=True)      
    subject = db.Column(db.String(50), primary_key=True)
    edgroup = db.Column(db.String(10), db.ForeignKey('edgroup.id'), primary_key=True)
    deadline = db.Column(db.DateTime)

    subjects = db.relationship('Test')
    groups = db.relationship('Edgroup')

    __table_args__ = (
        db.ForeignKeyConstraint([id, subject], [Test.id, Test.subject]), {}
    )

    def __repr__(self):
        return '{}, {}, {}, {}'.format(self.id, self.subject, self.edgroup, self.deadline)

class TestDeadlineView(ModelView):
    column_display_pk = True
    form_columns = ['id', 'subjects', 'groups', 'deadline']
    column_hide_backrefs = False

class TestPass(db.Model):
    __tablename__ = 'testpass'
    id = db.Column(db.Integer, primary_key=True)
    studentid = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    subject = db.Column(db.String(50), primary_key=True)
    mark = db.Column(db.Integer, nullable=True)

    students = db.relationship('Student')
    subjects = db.relationship('Test')

    __table_args__ = (
        db.ForeignKeyConstraint([id, subject], [Test.id, Test.subject]), {}
    )

    def __repr__(self):
        return '{}, {}, {}, {}'.format(self.id, self.studentid, self.subject, self.mark)

class TestPassView(ModelView):
    column_display_pk = True
    form_columns = ['id', 'students', 'subjects', 'mark']
    column_hide_backrefs = False

class LabworkPass(db.Model):
    __tablename__ = 'labworkpass'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50), primary_key=True)
    studentid = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    mark = db.Column(db.Integer, nullable=True)

    students = db.relationship('Student')
    subjects = db.relationship('Labwork')

    __table_args__ = (
        db.ForeignKeyConstraint([id, subject], [Labwork.id, Labwork.subject]), {}
    )

    def __repr__(self):
        return '{}, {}, {}, {}'.format(self.id, self.studentid, self.subject, self.mark)

class LabworkPassView(ModelView):
    column_display_pk = True
    form_columns = ['id',  'subjects', 'students', 'mark']
    column_hide_backrefs = False

class LabworkDeadline(db.Model):
    __tablename__ = 'labworkdeadline'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), primary_key=True)
    edgroup = db.Column(db.String(10), db.ForeignKey('edgroup.id'), primary_key=True)
    deadline = db.Column(db.DateTime)

    subjects = db.relationship('Labwork')
    groups = db.relationship('Edgroup')

    __table_args__ = (
        db.ForeignKeyConstraint([id, subject], [Labwork.id, Labwork.subject]), {}
    )

    def __repr__(self):
        return '{}, {}, {}, {}'.format(self.id, self.subject, self.edgroup, self.deadline)

class LabworkDeadlineView(ModelView):
    column_display_pk = True
    form_columns = ['id',  'subjects', 'groups', 'deadline']
    column_hide_backrefs = False

class Staff(db.Model):
    __tablename__ = 'staff'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    faculty = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))

    faculties = db.relationship('Faculty', backref='staff_fac')
    users = db.relationship('User')

    def __repr__(self):
        return '{}, {}, {}'.format(self.id, self.name, self.faculty)

class StaffView(ModelView):
    column_display_pk = True
    form_columns = ['id',  'name', 'faculties', 'users']
    column_hide_backrefs = False

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(50), unique=True)
    hash = db.Column(db.String(256), unique=True)
    role = db.Column(db.String(50))

    def set_password(self, password):
        self.hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash, password)

    def avatar(self, size):
        digest = md5(self.login.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return '{}, {}, {}'.format(self.id, self.login, self.role)

#endregion

@loginManager.user_loader
def load_user(id):
    return User.query.get(int(id))

class DbAdminHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/db_admin_main.html')

adminManager.add_view(DbAdminHomeView(name='Панель управления', endpoint='db_admin_main'))
adminManager.add_view(ModelView(User, db.session))
adminManager.add_view(EdgroupView(Edgroup, db.session))
adminManager.add_view(StudentView(Student, db.session))
adminManager.add_view(SubjectView(Subject, db.session))
adminManager.add_view(AssignedClassView(AssignedClass, db.session))
adminManager.add_view(TestView(Test, db.session))
adminManager.add_view(LabworkView(Labwork, db.session))
adminManager.add_view(TestDeadlineView(TestDeadline, db.session))
adminManager.add_view(TestPassView(TestPass, db.session))
adminManager.add_view(LabworkDeadlineView(LabworkDeadline, db.session))
adminManager.add_view(LabworkPassView(LabworkPass, db.session))
adminManager.add_view(StaffView(Staff, db.session))



