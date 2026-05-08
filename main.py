import os

from flask import Flask, redirect, render_template
from flask_login import LoginManager, login_required, login_user, logout_user

from data.db_session import create_session, global_init
from data.user import User
from forms.user import LoginForm, RegistationForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "6bbc695e03c4c4745fd786c943cb1d44"

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.get(User, user_id)


@app.route("/")
def index():
    return render_template("index.html", title="Главная страница")

@app.route("/catalog")
def catalog():
    return render_template("catalog.html", title="Каталог")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistationForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = User()
        user.email = form.email.data
        user.name = form.name.data
        user.set_password(form.password.data)

        db_sess.add(user)
        db_sess.commit()
        return redirect("/login")

    return render_template("register.html", title="Регистрация", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template(
            "login.html", message="Неправильный логин или пароль", form=form
        )
    return render_template("login.html", title="Авторизация", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    global_init("./db/database.db")
    app.run()


if __name__ == "__main__":
    os.makedirs("db", exist_ok=True)
    main()
