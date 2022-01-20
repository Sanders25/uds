from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_login(self, login):
        user = User.query.filter_by(login=login.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другой логин.')

    
