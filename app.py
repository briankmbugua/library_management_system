from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import LoginManager
from models import *
from flask_bcrypt import Bcrypt
from datetime import date, timedelta
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@localhost:3306/libdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = b'hkahs3720/'
bcrypt = Bcrypt(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
migrate = Migrate(app, db)

# with app.app_context():
#     # db.drop_all()
#     db.create_all()
#     # migrate.init()

# Create user loader callback that returns a user give the userID


@login_manager.user_loader
def loader_user(userID):
    return usersList.query.get(userID)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form['username']
#         password = request.form['password']
#         user = usersList.query.filter_by(userName=username).first()
#         if user and bcrypt.check_password_hash(user.password, password):
#             login_user(user)
@app.route("/register", methods=("POST", "GET"))
def register():
    if request.method == "POST":
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password'])
        user = usersList(userName=username,
                         password=password)
        db.session.add(user)
        db.session.commit()
        flash("Account created succesfully", "succes")
        return redirect(url_for("login"))
    elif request.method == "GET":
        return render_template("register.html")


@app.route("/addUser", methods=("POST", "GET"))
def addUser():
    if request.method == "POST":
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password'])
        usertype = request.form['userType']
        user = usersList(userName=username,
                         password=password, userType=usertype)
        db.session.add(user)
        db.session.commit()
        if user.userID:
            message = "User added successfully!"
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


@app.route("/addBook", methods=("POST", "GET"))
def addBook():
    if request.method == "POST":
        accNumber = request.form['accNumber']
        booktitle = request.form['booktitle']
        authorname = request.form['authorname']
        publishername = request.form['publishername']
        pages = request.form['pages']
        price = request.form['price']
        status = request.form['status']
        book = bookMaster(accNumber=accNumber, bookTitle=booktitle, authorName=authorname,
                          PublisherName=publishername, pages=pages, price=price, status=status)
        db.session.add(book)
        db.session.commit()
        if book.accNumber:
            message = "Book added successfully!"
            flash(message, "success")
        else:
            flash("Failed to add Book. Please try again")

        return render_template("index.html")
    elif request.method == "GET":
        # Subjects = Subjects.query.all()  # get all the subjects to populate the dropdwon
        return render_template("addBook.html")


@app.route("/deleteBook/<int:accNumber>")
def deleteBook(accNumber):
    book = bookMaster.query.get_or_404(accNumber)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/updateBook/<int:accNumber>", methods=['POST', 'GET'])
def updateBook(accNumber):
    book = bookMaster.query.get_or_404(accNumber)
    subjects = Subjects.query.all()

    if request.method == 'POST':
        book.accNumber = request.form['accNumber']
        book.bookTitle = request.form['booktitle']
        book.authorName = request.form['authorname']
        book.PublisherName = request.form['publishername']
        book.pages = request.form['pages']
        book.price = request.form['price']
        book.status = request.form['status']
        subname = request.form['subname']
        subject = Subjects.query.filter_by(subName=subname).first()
        book.SubID = subject.subID
        db.session.commit()
        return redirect(url_for('index'))
    else:
        # get all subjects to use in populating the select tag
        data = [subjects, book]
        return render_template('updateBook.html', data=data)


@app.route("/books")
def books():
    books = bookMaster.query.all()
    return render_template("allBooks.html", books=books)


@app.route("/booksBySubject/<int:id>")
def booksBySubject(id):
    # query the database for all books that have the specified subject ID.
    books = bookMaster.query.filter_by(SubID=id)
    return render_template('booksBySubject.html', books=books)


# def get_or_create(session, model, **kwargs):
#     instance = session.query(model).filter_by(**kwargs)
#     if instance is None:
#         instance = model(**kwargs)
#         session.add(instance)
#         session.commit()
#     return instance


# @app.route('/setBookSubject/<int:accNumber>')
# def setBookSubject(accNumber):
#     book = bookMaster.query.get_or_404(accNumber)
#     subName = request.form['subName']
#     subject = get_or_create(db.session, Subjects, subName=subName)
#     book.SubID = subject.subID
#     db.session.add(book)
#     db.session.commit()
#     return redirect(url_for('books'))

if __name__ == "__main__":
    app.run(debug=True)
