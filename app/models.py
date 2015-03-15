# -*- coding: utf-8 -*-
import uuid
import datetime
from app import db
from sqlalchemy.orm import relationship

from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    uuid = db.Column(db.String(64), unique = True)
    password = db.Column(db.String(500))
    name = db.Column(db.String(500))
    email = db.Column(db.String(120))

    def get_uuid(self):
        return self.uuid

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.uuid)

    def __init__(self, *args,**kwargs):
        super(User, self).__init__(*args,**kwargs)

        if kwargs.get('password'):
            self.set_password(kwargs.get('password'))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

class Bin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64))
    latitude = db.Column(db.DECIMAL(precision=6,scale=3,asdecimal=True))
    longitude = db.Column(db.DECIMAL(precision=6,scale=3,asdecimal=True))
    timestamp = db.Column(db.BigInteger())

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship('User',
        backref=db.backref('bins', lazy='dynamic'))

    def get_utc_created(self):
        return datetime.datetime.fromtimestamp(self.timestamp)