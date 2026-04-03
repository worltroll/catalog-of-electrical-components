from flask import Flask, render_template

app = Flask(__name__)
app.config["SECRET_KEY"] = "6bbc695e03c4c4745fd786c943cb1d44"


@app.route("/")
def hello():
    return render_template("index.html", title="main page")


if __name__ == "__main__":
    app.run(debug=True)
