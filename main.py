from flask import Flask, render_template, redirect
from flask_login import login_manager, login_user
from data.db_session import global_init, create_session
from data.user import User
from forms.user import RegistationForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "6bbc695e03c4c4745fd786c943cb1d44"


@app.route("/")
def index():
    return render_template("index.html", title="Главная страница")


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

    return render_template("register.html", title="Регистрация", form=form)


def main():
    global_init("./db/database.db")
    app.run()


if __name__ == "__main__":
    main()
