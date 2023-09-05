from flask import Flask, render_template, request, url_for, session, flash, redirect
from markupsafe import Markup
from models import *
from datetime import date, timedelta
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@localhost:3306/libdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = b'hkahs3720/'
db.init_app(app)
migrate = Migrate(app, db)

# with app.app_context():
#     # db.drop_all()
#     db.create_all()
#     migrate.init()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/addUser", methods=("POST", "GET"))
def addUser():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        usertype = request.form['userType']
        user = usersList(userName=username,
                         password=password, userType=usertype)
        db.session.add(user)
        db.session.commit()
        if user.userID:
            message = Markup("User added successfully!")
            flash(message, "success")
        else:
            flash("Failed to add user. Please try again")

        return render_template("index.html")
    elif request.method == "GET":
        return render_template("addUser.html")


@app.route("/deleteUser/<int:id>")
def deleteUser(id):
    user = usersList.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/updateUser/<int:id>", methods=['POST', 'GET'])
def updateUser(id):
    user = usersList.query.get_or_404(id)

    if request.method == 'POST':
        user.userName = request.form['name']
        user.userType = request.form['usertype']
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was an issue updating the user'
    else:
        return render_template('updateUser.html', user=user)


@app.route("/users")
def users():
    users = usersList.query.all()
    return render_template("allUsers.html", users=users)


@app.route("/addSubject", methods=("POST", "GET"))
def addSubject():
    if request.method == "POST":
        subject = request.form['subject']

        subject = Subjects(subName=subject)
        db.session.add(subject)
        db.session.commit()
        if subject.subID:
            flash("Subject added successfully")
        else:
            flash("Failed to add subject. Please try again")

        return render_template("index.html")
    elif request.method == "GET":
        return render_template("addSubject.html")


@app.route("/updateSubject/<int:id>", methods=['POST', 'GET'])
def updateSubject(id):
    subject = Subjects.query.get_or_404(id)

    if request.method == 'POST':
        subject.subName = request.form['subname']
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was an issue updating the subject'
    else:
        return render_template('updateSubject.html', subject=subject)


@app.route("/subjects")
def subjects():
    subjects = Subjects.query.all()
    return render_template("allSubjects.html", subjects=subjects)


@app.route("/deleteSubject/<int:id>")
def deleteSubject(id):
    subject = Subjects.query.get_or_404(id)
    db.session.delete(subject)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)