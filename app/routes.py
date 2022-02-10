# -*- coding: utf-8 -*-
from imghdr import tests
from re import S, T
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegisterForm, GroupSearchForm, EditTaskForm, RoleSelectForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import LabworkDeadline, User, Student, Subject, Labwork, Test, AssignedClass,\
                         LabworkDeadline, TestDeadline, Staff, Edgroup, LabworkPass, TestPass, Faculty
from werkzeug.urls import url_parse
from sqlalchemy import between, func, select, and_, DateTime
from sqlalchemy.sql.expression import literal
from sqlalchemy.orm import load_only
from datetime import datetime


@app.route('/')
@app.route('/index')
@login_required
def index():
    if current_user.is_authenticated:
        match current_user.role:
            case "admin":
                return redirect(url_for('admin_accounts'))
            case "db_admin":
                return redirect(url_for('db_admin_main'))
            case "staff":
                return redirect(url_for('staff_profile'))
            case "student":
                return redirect(url_for('student_profile'))
    elif current_user.is_anonymous:
        return redirect(url_for('login'))      

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user is None or not user.check_password(form.password.data) or user.role == None:
            flash('Неверные имя пользователя / пароль или администратор ещё не выдал Вам разрешение на вход.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Вход', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(login=form.login.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<login>')
@login_required
def user(login):
    user = User.query.filter_by(login=login).first_or_404()
    return render_template('user.html', user=user)

#region adminRoutes

@app.route('/admin_subjects/')
@login_required
def admin_subjects():
    return render_template('admin/admin_subjects.html')

@app.route('/admin_groups/')
@login_required
def admin_groups():
    return render_template('admin/admin_groups.html')
    
@app.route('/admin_accounts/', methods=['GET', 'POST'])
@login_required
def admin_accounts():

    roles = ['Преподаватели', 'Студенты']
    form = RoleSelectForm()
    form.role.choices = roles
    
    users = User.query.all()

    if request.method == "POST":
        selectedRole = request.form['role']
        selectedRole = 'Staff' if selectedRole == 'Преподаватели' else 'Student'

    return render_template('admin/admin_accounts.html', roles=roles, form=form, users=users)

@app.route('/db_admin_main')
@login_required
def db_admin_main():
    return render_template('admin/db_admin_main.html')

#endregion

#region staffRoutes

@app.route('/staff_profile/')
@login_required
def staff_profile():
    user = User.query.filter_by(login=current_user.login).first()
    staff = Staff.query.filter(Staff.userId == user.id).first()
    subject = Subject.query.filter(Subject.staffId == staff.id).first()
    print(staff)
    return render_template('staff/staff_profile.html', title='Профиль', faculty=staff.faculty, user=user, name=staff.name, subject=subject)

@app.route('/staff_manage', methods=['GET', 'POST'])
@login_required
def staff_manage():
    user = User.query.filter_by(login=current_user.login).first()
    staffInfo = Staff.query.filter(Staff.userId == user.id).first()

    #? Запрос, возвращающий предмет, который ведёт данный преподватель
    subj = db.session.query(Subject).filter(Subject.staffId == staffInfo.id).first()
    #?
    #? Запрос, возвращающий группы, у которых данный преподватель ведёт предмет subj
    groups = db.session.query(AssignedClass.edgroup).filter(AssignedClass.subject == subj.name).all()
    #?

    groups = [r for r, in groups]
    #form = GroupSearchForm()
    #form.choices = [groups]

    selectedGroup = groups[0]

    if request.method == "POST":
        selectedGroup = request.form['groupSelect']
        
    # TODO: Здесь выводится список группы, где каждый студент кликабелен. Можно 
    #* также подсчитывать количество сданных работ для каждого студента.
    #* Нажимая на студента должны выводиться все работы для группы данного студента
    # TODO

    students = db.session.query(Student).filter(Student.edgroup == selectedGroup).all()
    return render_template('staff/staff_manage.html', groups=groups, students=students, selectedGroup=selectedGroup, subj=subj.name)


@app.route('/staff_manage/<subj>/<group>/<student>')
@login_required
def ShowStudentTasks(student, subj, group):
    studentName = Student.query.with_entities(Student.name).filter(Student.id == student).all()
    studentName = [n for n, in studentName]

    #labworks = LabworkPass.query.join(Labwork).with_entities(Labwork.id.label('labNum'), Labwork.name.label('labName'), LabworkPass.mark).filter(LabworkPass.subject == subj, LabworkPass.studentid == student).all()
    marks = LabworkPass.query.join(Labwork).with_entities(Labwork.id.label('labNum'), Labwork.name.label('labName'), LabworkPass.mark).filter(LabworkPass.subject == subj, LabworkPass.studentid == student).subquery()
    deadlines = LabworkDeadline.query.join(Labwork).with_entities(Labwork.id, LabworkDeadline.deadline).filter(LabworkDeadline.subject == subj, LabworkDeadline.edgroup == group).subquery()
    labworks = db.session.query(deadlines, marks.c.labNum, marks.c.labName, marks.c.mark).join(marks, marks.c.labNum == deadlines.c.id).all()

    #? Все работы, приписанные данному студенту
    #grTests = TestDeadline.query.with_entities(TestDeadline.id.label('testNum'), Test.name.label('testName'), TestDeadline.subject.label('testSubject'))\
    #.join(Test).filter(TestDeadline.subject == subj, TestDeadline.edgroup == group).subquery('grTests')
    #?
    #? Оценки, полученные за данные работы
    marks = TestPass.query.join(Test).with_entities(Test.id.label('testNum'), Test.name.label('testName'), TestPass.mark).filter(TestPass.subject == subj, TestPass.studentid == student).subquery()
    deadlines = TestDeadline.query.join(Test).with_entities(Test.id, TestDeadline.deadline).filter(TestDeadline.subject == subj, TestDeadline.edgroup == group).subquery()
    tests = db.session.query(deadlines, marks.c.testNum, marks.c.testName, marks.c.mark).join(marks, marks.c.testNum == deadlines.c.id).all()
    #?      
    for mark in tests:
        print(mark)

    return render_template('/staff/staff_stud_tasks.html', labworks=labworks, tests=tests, subj=subj, studentName=studentName[0])

@app.route('/manage_tasks/')
@login_required
def ManageTasks():

    # TODO Нужно нормально всё выводить тут

    user = db.session.query(Staff).filter(Staff.userId == current_user.id).first()
    subject = Subject.query.filter(Subject.staffId == user.id).first()

    #labs = Labwork.query.filter(Labwork.subject == subject.name).join(LabworkDeadline).all()
    labs = Labwork.query.with_entities(Labwork.id, Labwork.name, LabworkDeadline.edgroup, LabworkDeadline.deadline).filter(Labwork.subject == subject.name).join(LabworkDeadline, and_(Labwork.id == LabworkDeadline.id, Labwork.subject == LabworkDeadline.subject)).all()
    tests = Test.query.with_entities(Test.id, Test.name, TestDeadline.edgroup, TestDeadline.deadline).filter(Test.subject == subject.name).join(TestDeadline, and_(Test.id == TestDeadline.id, Test.subject == TestDeadline.subject)).all()
    return render_template('/staff/manage_tasks.html', labs=labs, tests=tests, subject=subject)

@app.route('/edit_lab/<subject>/<group>/<id>', methods=['GET', 'POST'])
@login_required
def EditLab(id, subject, group):
    lab = db.session.query(LabworkDeadline, Labwork.name, func.to_char(LabworkDeadline.deadline, 'DD-MM-YYYY HH24:MI:SS').label('datetime'), Labwork.commentary).join(Labwork).filter(LabworkDeadline.id == id, LabworkDeadline.subject == subject, LabworkDeadline.edgroup == group).first()
    groups = AssignedClass.query.with_entities(AssignedClass.edgroup).filter(AssignedClass.subject == subject).all()
    groups = [g for g, in groups]
    print(lab)

    form = EditTaskForm(taskId=id, taskName=lab.name, taskGroup=group, taskDeadline=datetime.strptime(lab.datetime, '%d-%m-%Y %H:%M:%S') , taskCommentary=lab.commentary);
    form.taskGroup.choices = [(group, group) for group in groups]

    if request.method == "POST":
        lId = request.form['taskId']
        lName = request.form['taskName']
        lGroup = request.form['taskGroup']
        lDeadline = request.form['taskDeadline']
        lCommentary = request.form['taskCommentary']
        db.session.query(Labwork).filter(Labwork.id == id, Labwork.subject == subject).update({"id":(lId), "name":(lName), "commentary":(lCommentary)})
        db.session.commit()
        db.session.query(LabworkDeadline).filter(LabworkDeadline.id == id, LabworkDeadline.subject == subject, LabworkDeadline.edgroup == group).update({"edgroup":(lGroup), "deadline":(lDeadline)})
        db.session.commit()
        return redirect(url_for('ManageTasks'))

    return render_template('/staff/edit_lab.html', form=form)

@app.route('/edit_test/<subject>/<group>/<id>', methods=['GET', 'POST'])
@login_required
def EditTest(id, subject, group):
    test = Test.query.filter(Test.id == id, Test.subject == subject).first()
    form = EditTaskForm(taskId = test.id, taskName = test.name);

    if request.method == "POST":
        tId = request.form['taskId']
        tName = request.form['taskName']
        db.session.query(Test).filter(Test.id == tId, Test.subject == subject).update({"id":(tId), "name":(tName)})
        db.session.commit()
        return redirect(url_for('ManageTasks'))

    return render_template('/staff/edit_test.html', form=form)

@app.route('/add_test/<subject>', methods=['GET', 'POST'])
@login_required
def AddTest(subject):
    test = db.session.query(func.max(Test.id)).filter(Test.subject == subject).first()
    form = EditTaskForm(taskId = test[0] + 1);

    if request.method == "POST":
        tId = request.form['taskId']
        tName = request.form['taskName']
        t = Test(id=tId, name=tName, subject=subject)
        db.session.add(t)
        db.session.commit()
        return redirect(url_for('ManageTasks'))

    return render_template('/staff/add_test.html', form=form)

@app.route('/add_lab/<subject>', methods=['GET', 'POST'])
@login_required
def AddLab(subject):
    
    lab = db.session.query(func.max(Labwork.id)).filter(Labwork.subject == subject).first()
    groups = AssignedClass.query.with_entities(AssignedClass.edgroup).filter(AssignedClass.subject == subject).all()

    groups = [g for g, in groups]
    #? Находит номер последней работы и выводит следующий за ним
    form = EditTaskForm(taskId = lab[0] + 1)
    form.taskGroup.choices = [(group, group) for group in groups]


    if request.method == "POST":
        tId = request.form['taskId']
        tName = request.form['taskName']
        tGroup = request.form['taskGroup']
        tDeadline = request.form['taskDeadline']
        l = Labwork(id=tId, name=tName, subject=subject)
        ld = LabworkDeadline(id=tId, subject=subject, edgroup=tGroup, deadline=tDeadline)
        db.session.add(l)
        db.session.add(ld)
        db.session.commit()
        return redirect(url_for('ManageTasks'))

    return render_template('/staff/add_lab.html', form=form)

@app.route('/delete_lab/<subject>/<group>/<id>', methods=['GET', 'POST'])
@login_required
def DeleteLab(subject, group, id):
    l = Labwork.query.filter(Labwork.id == id, Labwork.subject == subject).first()
    db.session.delete(l)
    return redirect(url_for('ManageTasks'))

@app.route('/delete_test/<subject>/<group>/<id>', methods=['GET', 'POST'])
@login_required
def DeleteTest(subject, group, id):
    t = Test.query.filter(Test.id == id, Test.subject == subject).first()
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for('ManageTasks'))
#endregion

#region studentRoutes

@app.route('/student_profile')
@login_required
def student_profile():
    user = User.query.filter_by(login=current_user.login).first()
    student = Student.query.filter(Student.userId == user.id).first()
    faculty = Faculty.query.join(Edgroup).filter(Edgroup.id == student.edgroup).first()
    return render_template('student/student_profile.html', title="Профиль", group=student.edgroup, student=student, user=user, id=student.id, name=student.name, faculty=faculty.name)

@app.route('/student_tasks')
@login_required
def student_tasks():
    user = User.query.filter_by(login=current_user.login).first()
    student = Student.query.filter(Student.userId == user.id).first()

    #? Запрос, возвращающий информацию о лабораторных, идущих у данного студента
    subq = LabworkPass.query.filter(LabworkPass.studentid == student.id).subquery()
    subq2 = LabworkDeadline.query.with_entities(LabworkDeadline.id, LabworkDeadline.subject, subq.c.mark, LabworkDeadline.deadline).outerjoin(subq, and_(subq.c.id == LabworkDeadline.id, subq.c.subject == LabworkDeadline.subject)).filter(LabworkDeadline.edgroup == student.edgroup).subquery()
    labworks = Labwork.query.with_entities(Labwork.id, Labwork.subject, Labwork.name.label('labName'), subq2.c.mark, ((subq2.c.mark * 100) / 5).label('percent'), func.to_char(subq2.c.deadline, 'DD.MM.YYYY').label('deadline'), Staff.name.label('instructor')).join(subq2, and_(subq2.c.id == Labwork.id, subq2.c.subject == Labwork.subject)).outerjoin(Subject, Labwork.subject == Subject.name).outerjoin(Staff, Subject.staffId == Staff.id).all()
    
    #? Запрос, возвращающий всю информацию о контрольных, идущих у данного студента
    subq = TestPass.query.filter(TestPass.studentid == student.id).subquery()
    subq2 = TestDeadline.query.with_entities(TestDeadline.id, TestDeadline.subject, subq.c.mark, TestDeadline.deadline).outerjoin(subq, and_(subq.c.id == TestDeadline.id, subq.c.subject == TestDeadline.subject)).filter(TestDeadline.edgroup == student.edgroup).subquery()
    tests = Test.query.with_entities(Test.id, Test.subject, Test.name.label('testName'), subq2.c.mark, ((subq2.c.mark * 100) / 5).label('percent'), subq2.c.deadline, Staff.name.label('instructor')).join(subq2, and_(subq2.c.id == Test.id, subq2.c.subject == Test.subject)).outerjoin(Subject, Test.subject == Subject.name).outerjoin(Staff, Subject.staffId == Staff.id).all()
    #?

    print(labworks)

    return render_template('student/student_tasks.html', title="Задания", labworks=labworks, tests=tests)

@app.route('/student_tasks/<instructor>')
@login_required
def ShowInstructorProfile(instructor):

    staffInfo = Staff.query.filter(Staff.name == instructor).first()
    user = User.query.filter(User.id == staffInfo.userId).first()
    subject = Subject.query.filter(Subject.staffId == staffInfo.id).first()
        
    return render_template('student/instructor_profile.html', title="Преподаватель", staffInfo=staffInfo, user=user, subject=subject)
#endregion