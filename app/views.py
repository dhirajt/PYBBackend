# -*- encoding: utf-8 -*-

from flask import (url_for, redirect, render_template, flash, g,
    session, request, jsonify)
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, lm, db
from forms import ExampleForm, LoginForm

from .models import User, Bin

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def get_or_create(session, model, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

@app.route('/save/location/', methods = ['GET','POST'])
def index():
    if request.json:
        user = None
        count = 0
        for data in request.json:
            if not user:
                user = get_or_create(db.session,User,uuid=data['device_id'])
                db.session.add(user)

            dust_bin = get_or_create(db.session,Bin,
                uuid=data['device_id'],latitude=data['latitude'],
                longitude=data["longitude"],timestamp=data['timestamp'],
                user=user)
            count += 1

            db.session.add(dust_bin)
        db.session.commit()

        response =  jsonify(status="success",message="locations saved")
        return response

    response = jsoniify(status="error",message="wrong request type",
        status_code=400)
    return response

# === User login methods ===

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

#@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        login_user(g.user)

    return render_template('login.html',
        title = 'Sign In',
        form = form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))
