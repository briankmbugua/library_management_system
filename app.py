from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import *
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, timedelta
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@localhost:3306/libdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = b'hkahs3720/'
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


# login route to handle user login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = usersList.query.filter_by(userName=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in succesfully", "succes")
            return redirect(url_for("index"))
        else:
            flash("Login failed. Check your username and password")
    return render_template("login.html")


@app.route("/logout")
@login_required  # Ensure that only authenticated users can log out
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=("POST", "GET"))
def register():
    if request.method == "POST":
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        library_name = request.form['library']
        library = Library(name=library_name)
        user = usersList(userName=username,
                         password=password, userType="admin", library=library)
        db.session.add(user)
        db.session.add(library)
        db.session.commit()
        flash("Account created succesfully", "succes")
        return redirect(url_for("login"))
    elif request.method == "GET":
        return render_template("register.html")


# for the librarian to add users to their specific library
@app.route("/addUser", methods=("POST", "GET"))
@login_required
def addUser():
    if request.method == "POST":
        username = request.form['username']
        usertype = request.form['userType']

        # get the currently logged in librarian
        current_library = current_user.library
        user = usersList(userName=username,
                         userType=usertype, library=current_library)
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
@login_required
def deleteUser(id):
    user_to_delete = usersList.query.filter_by(
        library=current_user.library, id=id).first_or_404()
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/updateUser/<int:id>", methods=['POST', 'GET'])
@login_required
def updateUser(id):
    user_to_update = usersList.query.filter_by(
        library=current_user.library, id=id).first_or_404()

    if user_to_update.library == current_user.library:
        if request.method == 'POST':
            user_to_update.userName = request.form['name']
            user_to_update.userType = request.form['usertype']
            try:
                db.session.commit()
                return redirect(url_for('index'))
            except:
                return 'There was an issue updating the user'
    else:
        return render_template('updateUser.html', user=user_to_update)


@app.route("/users")
@login_required
def users():
    users = usersList.query.filter_by(library=current_user.library).all()
    return render_template("allUsers.html", users=users)


@app.route("/addSubject", methods=("POST", "GET"))
@login_required
def addSubject():
    if request.method == "POST":
        subject = request.form['subject']
        library = current_user.library
        subject = Subjects(subName=subject, library=library)
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
@login_required
def updateSubject(id):
    subject = Subjects.query.filter_by(
        id=id, library=current_user.library).first_or_404()

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
@login_required
def subjects():
    subjects = Subjects.query.filter_by(library=current_user.library).all()
    return render_template("allSubjects.html", subjects=subjects)


@app.route("/deleteSubject/<int:id>")
@login_required
def deleteSubject(id):
    subject = Subjects.query.get_or_404(id)
    db.session.delete(subject)
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/addBook", methods=("POST", "GET"))
@login_required
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
                          PublisherName=publishername, pages=pages, price=price, status=status, library=current_user.library)
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
@login_required
def deleteBook(accNumber):
    book = bookMaster.query.filter_by(
        accNumber=accNumber, library=current_user.library).first_or_404()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/updateBook/<int:accNumber>", methods=['POST', 'GET'])
@login_required
def updateBook(accNumber):
    book = bookMaster.query.filter_by(
        accNumber=accNumber, library=current_user.library).first_or_404()
    subjects = Subjects.query.filter_by(library=current_user.library).all()

    if request.method == 'POST':
        book.accNumber = request.form['accNumber']
        book.bookTitle = request.form['booktitle']
        book.authorName = request.form['authorname']
        book.PublisherName = request.form['publishername']
        book.pages = request.form['pages']
        book.price = request.form['price']
        book.status = request.form['status']
        subname = request.form['subname']
        subject = Subjects.query.filter_by(
            subName=subname, library=current_user.library).first()
        book.SubID = subject.subID
        db.session.commit()
        return redirect(url_for('index'))
    else:
        # get all subjects to use in populating the select tag
        data = [subjects, book]
        return render_template('updateBook.html', data=data)


@app.route("/books")
@login_required
def books():
    books = bookMaster.query.filter_by(library=current_user.library).all()
    return render_template("allBooks.html", books=books)


@app.route("/booksBySubject/<int:id>")
@login_required
def booksBySubject(id):
    # query the database for all books that have the specified subject ID.
    books = bookMaster.query.filter_by(SubID=id, library=current_user.library)
    return render_template('booksBySubject.html', books=books)


if __name__ == "__main__":
    app.run(debug=True)
