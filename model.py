from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True, autoincrement =True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    user_type = db.Column(db.String)
   

class User_theater_relation(db.Model):
    __tablename__ = 'User_theater_relation'
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    theater_id=db.Column(db.Integer, db.ForeignKey('theaters.id'), primary_key = True)

class theaters(db.Model):
    __tablename__ = 'theaters'
    id = db.Column(db.Integer, primary_key = True, autoincrement =True)
    name = db.Column(db.String)
    status = db.Column(db.Boolean, default=False)
    user_id = db.relationship('users', secondary = 'User_theater_relation')



class movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key = True, autoincrement =True)
    name = db.Column(db.String, unique=True)
    genre = db.Column(db.String )
    poster = db.Column(db.String )
    
