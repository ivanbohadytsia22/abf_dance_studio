from flask import Flask,render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/header")
def header():
    return render_template("header.html")


if __name__ == "__main__":
    app.run(debug=True)