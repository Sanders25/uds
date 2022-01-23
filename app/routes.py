# -*- coding: utf-8 -*-
from re import S
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import LabworkDeadline, User, Student, Subject, Labwork, Test, AssignedClass, LabworkDeadline, TestDeadline
from werkzeug.urls import url_parse

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
    return render_template('staff/staff_profile.html')

@app.route('/staff_manage')
@login_required
def staff_manage():
    return render_template('admin/staff_manage.html')

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

    #subq = db.session.query(LabworkDeadline.id, LabworkDeadline.edgroup, LabworkDeadline.deadline, LabworkDeadline.subject).filter(LabworkDeadline.edgroup == student.edgroup).distinct().all()
    subq = db.session.query(LabworkDeadline.id, LabworkDeadline.edgroup, LabworkDeadline.deadline, LabworkDeadline.subject).filter(LabworkDeadline.edgroup == student.edgroup).subquery('subq')
    labworks = db.session.query(subq, Labwork.name).join(Labwork).all()

    #for i in subq:
    #    print(i)

    subq = db.session.query(TestDeadline.id, TestDeadline.edgroup, TestDeadline.deadline).filter(TestDeadline.edgroup == student.edgroup).distinct().subquery('subq')
    tests = db.session.query(subq, Test.name, Test.subject).join(Test).all()

    return render_template('student/student_tasks.html', title="Задания", labworks=labworks, tests=tests)

#endregion