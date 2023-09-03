from flask import Flask, render_template, request, url_for, session
from models import *
from datetime import date, timedelta

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@localhost:3306/libdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = b'hkahs3720/'
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/addUser", methods=("POST", "GET"))
def addUser():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        usertype = request.form['userType']

        fakeuser = [username, password, usertype]

        user = usersList(userName=username,
                         password=password, userType=usertype)
        db.session.add(user)
        db.session.commit()

        return render_template("index.html", user=fakeuser)
    elif request.method == "GET":
        return render_template("addUser.html")


@app.route("/addSubject", methods=("POST", "GET"))
def addSubject():
    if request.method == "POST":
        subject = request.form['subject']

        fakesubject = [subject]

        subject = Subjects(subName=subject)
        db.session.add(subject)
        db.session.commit()

        return render_template("index.html", subject=fakesubject)
    elif request.method == "GET":
        return render_template("addSubject.html")


if __name__ == "__main__":
    app.run(debug=True)
