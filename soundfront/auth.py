from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for, current_app)
import hashlib

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        password_repeat = request.form['password_repeat']
        error = None

        if not email:
            error = 'Email is required.'
        elif not name:
            error = 'Name is required'
        elif not password:
            error = 'Password is required'
        elif not password == password_repeat:
            error = 'Passwords do not match.'

        if error is None:
            user_repo = current_app.config['user']
            user = user_repo.create_user(email, name, password)
            session['user_id'] =  user.UserID
            return redirect(url_for('index.index'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            user_repo = current_app.config['user']
            user = user_repo.get_user_by_email(email)

            if user is None:
                error = 'User does not exist with that email.'
            else:
                valid = user_repo.check_login(email, password)

                if valid is None:
                    error = 'Invalid password'

        if error is None:
            session.clear()
            session['user_id'] =  user.UserID
            return redirect(url_for('index.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index.index'))
