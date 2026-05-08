from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField, PasswordField, StringField, BooleanField, validators


class RegistationForm(FlaskForm):
    email = EmailField("Эл. Почта", validators=[validators.DataRequired()])
    password = PasswordField("Пароль", validators=[validators.DataRequired()])
    name = StringField("Имя")
    confirm = PasswordField(
        "Повторите пароль",
        validators=[
            validators.DataRequired(),
            validators.EqualTo("password", message="Пароли должны совпадать"),
        ],
    )
    submit = SubmitField("Зарегистрироваться")

class LoginForm(FlaskForm):
    email = EmailField('Эл. Почта', validators=[validators.DataRequired()])
    password = PasswordField('Пароль', validators=[validators.DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')