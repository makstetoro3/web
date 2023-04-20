from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    login = StringField('Логин для входа', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
