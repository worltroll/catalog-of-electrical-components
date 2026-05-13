import os

from flask import Flask, jsonify, make_response, redirect, render_template, request
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from data import users_api
from data.db_session import create_session, global_init
from data.users import User
from forms.user import EditUserForm, LoginForm, RegistationForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "6bbc695e03c4c4745fd786c943cb1d44"

login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({"error": "Bad Request"}), 400)


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
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Пользователь с таким email уже существует",
            )
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


@app.route("/account", methods=["GET", "POST"])
def account():
    db_sess = create_session()
    user = db_sess.get(User, current_user.id)
    if not user:
        return redirect("/")
    form = EditUserForm()
    if form.validate_on_submit():
        user.name = form.name.data
        if form.password.data:
            user.set_password(form.password.data)
        if form.image.data:
            os.makedirs(f"static/img/user/{user.id}/", exist_ok=True)
            try:
                os.remove(f"static/img/user/{user.id}/user_img.png")
            except Exception:
                pass
            file = form.image.data
            file.save(f"static/img/user/{user.id}/user_img.png")
            user.image = f"/static/img/user/{user.id}/user_img.png"
        db_sess.commit()
        return redirect("/")
    elif request.method == "GET":
        form.name.data = user.name
        form.email.data = user.email
    return render_template("account.html", title="Данные аккаунта", form=form)


def main():
    global_init("./db/database.db")
    app.register_blueprint(users_api.blueprint)
    app.run()


if __name__ == "__main__":
    os.makedirs("db", exist_ok=True)
    main()
