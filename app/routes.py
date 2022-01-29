# -*- coding: utf-8 -*-
from imghdr import tests
from re import S, T
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegisterForm, GroupSearchForm, EditTaskForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import LabworkDeadline, User, Student, Subject, Labwork, Test, AssignedClass,\
                         LabworkDeadline, TestDeadline, Staff, Edgroup, LabworkPass, TestPass
from werkzeug.urls import url_parse
from sqlalchemy import func
from sqlalchemy.sql.expression import literal
from sqlalchemy.orm import load_only


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
        if user is None or not user.check_password(form.password.data):
            flash('Неверные имя пользователя или пароль')
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
    
@app.route('/admin_accounts/')
@login_required
def admin_accounts():
    return render_template('admin/admin_accounts.html')

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
    print(staff)
    return render_template('staff/staff_profile.html', title='Профиль', faculty=staff.faculty, user=user, name=staff.name)

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

    labworks = LabworkPass.query.join(Labwork).with_entities(Labwork.id.label('labNum'), Labwork.name.label('labName'), LabworkPass.mark).filter(LabworkPass.subject == subj, LabworkPass.studentid == student).all()


    #? Все работы, приписанные данному студенту
    #grTests = TestDeadline.query.with_entities(TestDeadline.id.label('testNum'), Test.name.label('testName'), TestDeadline.subject.label('testSubject'))\
    #.join(Test).filter(TestDeadline.subject == subj, TestDeadline.edgroup == group).subquery('grTests')
    #?
    #? Оценки, полученные за данные работы
    marks = TestPass.query.join(Test).with_entities(Test.id.label('testNum'), Test.name.label('testName'), TestPass.mark).filter(TestPass.subject == subj, TestPass.studentid == student).subquery()
    deadlines = TestDeadline.query.join(Test).with_entities(Test.id, TestDeadline.deadline).filter(TestDeadline.subject == subj, TestDeadline.edgroup == group).subquery()
    tests = db.session.query(deadlines, marks.c.testNum, marks.c.testName, marks.c.mark).join(marks, marks.c.testNum == deadlines.c.id).all()
    #?        

    return render_template('/staff/staff_stud_tasks.html', labworks=labworks, tests=tests, subj=subj, studentName=studentName[0])

@app.route('/manage_tasks/')
@login_required
def ManageTasks():

    user = db.session.query(Staff).filter(Staff.userId == current_user.id).first()
    subject = Subject.query.filter(Subject.staffId == user.id).first()

    labs = Labwork.query.filter(Labwork.subject == subject.name)
    tests = Test.query.filter(Test.subject == subject.name)

    return render_template('/staff/manage_tasks.html', labs=labs, tests=tests, subject=subject)

@app.route('/edit_lab/<subject>/<id>')
@login_required
def EditLab(id, subject):

    form = EditTaskForm();

    lab = Labwork.query.filter(Labwork.id == id, Labwork.subject == subject).first()
    form.id = lab.id
    form.name = lab.name

    if request.method == "POST":
        lId = request.form['taskId']
        lName = request.form['taskName']
        db.session.query(Labwork).filter(Labwork.id == lId, Labwork.subject == subject).update({"id":(lId), "name":(lName)})
        db.session.commit()
        return redirect(url_for('ManageTasks'))

    return render_template('/staff/edit_lab.html', form=form)

@app.route('/edit_test/<subject>/<id>', methods=['GET', 'POST'])
@login_required
def EditTest(id, subject):
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
    lab = Labwork.query.filter(func.max(Labwork.id), Labwork.subject == subject).first()
    form = EditTaskForm(taskId = lab.id + 1);

    if request.method == "POST":
        tId = request.form['taskId']
        tName = request.form['taskName']
        l = Labwork.query.filter(id=tId, name=tName, subject=subject)
        db.session.add(l)
        db.session.commit()
        return redirect(url_for('ManageTasks'))

    return render_template('/staff/add_lab.html', form=form)

@app.route('/delete_lab/<subject>/<id>', methods=['GET', 'POST'])
@login_required
def DeleteLab(subject, id):
    l = Labwork.query.filter(Labwork.id == id, Labwork.subject == subject).first()
    db.session.delete(l)
    return redirect(url_for('ManageTasks'))

@app.route('/delete_test/<subject>/<id>', methods=['GET', 'POST'])
@login_required
def DeleteTest(subject, id):
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
    return render_template('student/student_profile.html', title="Профиль", group=student.edgroup, student=student, user=user, id=student.id, name=student.name)

@app.route('/student_tasks')
@login_required
def student_tasks():
    user = User.query.filter_by(login=current_user.login).first()
    student = Student.query.filter(Student.userId == user.id).first()

    #? Запрос, возвращающий информацию о лабораторных, идущих у данного студента

    studentLabworks = db.session.query(LabworkDeadline).filter(LabworkDeadline.edgroup == student.edgroup).subquery('studentLabworks')
    labworkInfo = db.session.query(studentLabworks, Labwork.id.label('labworkNum'), Labwork.name.label('labworkName')).join(Labwork).filter(Labwork.id == studentLabworks.c.id, Labwork.subject == studentLabworks.c.subject).subquery('labworkInfo')
    #? Запрос, возвращающий имена преподавателей предметов, идущих у данного студента
    labworks = db.session.query(labworkInfo, Staff.name.label('instructor')).join(Subject, labworkInfo.c.subject == Subject.name).join(Staff, Subject.staffId == Staff.id).all()
    #?
    #? Запрос, возвращающий информацию о контрольных, идущих у данного студента
    studentTests = db.session.query(TestDeadline).filter(TestDeadline.edgroup == student.edgroup).subquery('studentTests')
    testInfo = db.session.query(studentTests, Test.id.label('testNum'), Test.name.label('testName')).join(Test).filter(Test.id == studentTests.c.id, Test.subject == studentTests.c.subject).subquery('testInfo')
    tests = db.session.query(testInfo, Staff.name.label('instructor')).join(Subject, testInfo.c.subject == Subject.name).join(Staff, Subject.staffId == Staff.id).all()
    #?
    
    #? Объединение запросов
    #tasks = db.session.query(labworks, tests).join(tests, literal(True)).all()
    #?

    return render_template('student/student_tasks.html', title="Задания", labworks=labworks, tests=tests)

@app.route('/student_tasks/<instructor>')
@login_required
def ShowInstructorProfile(instructor):

    staffInfo = Staff.query.filter(Staff.name == instructor).first()
    user = User.query.filter(Staff.userId == User.id).first()
    subject = Subject.query.filter(Subject.staffId == staffInfo.id).first()
        
    return render_template('student/instructor_profile.html', title="Преподаватель", staffInfo=staffInfo, user=user, subject=subject)
#endregion