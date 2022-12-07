from marshmallow import Schema, fields
from setup_db import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String(200))
    surname = db.Column(db.String(200))
    favorite_genre = db.Column(db.Integer, db.ForeignKey('genre.id'))


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    password = fields.Str(load_only=True)
    name = fields.Str()
    surname = fields.Str()
    favorite_genre = fields.Str()
