from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField, PasswordField, StringField, BooleanField, validators


class RegistationForm(FlaskForm):
    email = EmailField("Email", validators=[validators.DataRequired()])
    password = PasswordField("Password", validators=[validators.DataRequired()])
    name = StringField("Name")
    confirm = PasswordField(
        "Repeat password",
        validators=[
            validators.DataRequired(),
            validators.EqualTo("password", message="Passwords need to match"),
        ],
    )
    submit = SubmitField("Зарегистрироваться")

class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[validators.DataRequired()])
    password = PasswordField('Пароль', validators=[validators.DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')