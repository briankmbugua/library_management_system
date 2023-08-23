from flask import Flask, render_template, jsonify, request, redirect, flash, url_for, session

from models import db, usersList, Subjects, IssueReturn, bookMaster

from datetime import date, timedelta

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@localhost:3306/libraryDB"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'my_secret_key'
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/logout")
def logout():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
