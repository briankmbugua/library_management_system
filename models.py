from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()


class Subjects(db.Model):
    __tablename__ = "Subjects"
    subID = db.Column(db.Integer, primary_key=True)
    subName = db.Column(db.String(50), nullable=False)


class usersList(db.Model, UserMixin):
    __tablename__ = "users"
    userID = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    userType = db.Column(db.String(50), nullable=True)


class bookMaster(db.Model):
    __tablename__ = "bookMaster"
    accNumber = db.Column(db.String(50), primary_key=True)
    bookTitle = db.Column(db.String(50), nullable=False)
    SubID = db.Column(db.Integer, db.ForeignKey(
        "Subjects.subID"), nullable=True)
    authorName = db.Column(db.String(50), nullable=False)
    PublisherName = db.Column(db.String(50), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer)
    status = db.Column(db.String(50))
    subject = db.relationship("Subjects", backref="subject", lazy=True)


class IssueReturn(db.Model):
    __tablename__ = "IssueReturn"
    transID = db.Column(db.Integer, primary_key=True)
    AccNumber = db.Column(db.String(50), db.ForeignKey(
        "bookMaster.accNumber"), nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey(
        "users.userID"), nullable=False)
    IssueDate = db.Column(db.Date, nullable=False)
    ExpRetDate = db.Column(db.Date, nullable=False)
    ActRetDate = db.Column(db.Date, nullable=False)
    OverdueDays = db.Column(db.Integer, nullable=False)
    book = db.relationship("bookMaster", backref="book", lazy=True)
    usr = db.relationship("usersList", backref="user", lazy=True)
