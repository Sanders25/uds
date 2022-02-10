from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()], render_kw={"placeholder": "Логин"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"placeholder": "Пароль"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()], render_kw={"placeholder": "Логин"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"placeholder": "Пароль"})
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Повторите пароль"})
    submit = SubmitField('Зарегистрироваться')

    def validate_login(self, login):
        user = User.query.filter_by(login=login.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другой логин.')

class GroupSearchForm(FlaskForm):
    group = SelectField('group', choices=[])

class RoleSelectForm(FlaskForm):
    role = SelectField('role', choices=[])
    submit = SubmitField('Применить')

class EditTaskForm(FlaskForm):
    taskId = StringField('Номер задания', validators=[DataRequired()])
    taskName = StringField('Название', validators=[DataRequired()])
    taskGroup = SelectField('Группа', validators=[DataRequired()], choices=[])
    taskDeadline = DateTimeLocalField('Срок до', format='%Y-%m-%dT%H:%M:%S', validators=[DataRequired()])
    taskCommentary = StringField('Комментарий')
    submit = SubmitField('Сохранить')



    
