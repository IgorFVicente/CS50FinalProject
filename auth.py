import functools
from datetime import datetime, date

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from myproject.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        email_confirm = request.form['email_confirm']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'E-mail is required.'
        elif not password:
            error = 'Password is required.'
        elif len(username) < 6:
            error = 'Username is too short.'
        elif len(password) < 6 or not any(str.isdigit(c) for c in password) or not any(str.isalpha(c) for c in password):
            error = 'Password must contain at least one number and one letter and must be at least six characters long.'
        elif email != email_confirm:
            error = 'The confirmation e-mail doesnt match.'
        elif password != password_confirm:
            error = "The provided passwords don't match."
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
        elif db.execute(
            'SELECT id FROM user WHERE email = ?', (email,)
        ).fetchone() is not None:
            error = 'Email {} is already registered.'.format(email)

        if error is None:
            db.execute (
                'INSERT INTO user (username, email, password) VALUES (?, ?, ?)',
                (username, email, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))
    
        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        identification = request.form['identification']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (identification,)
        ).fetchone()

        if user is None:
            user = db.execute(
                'SELECT * FROM user WHERE email = ?', (identification,)
            ).fetchone()
        if user is None:
            error = 'Incorrect username or email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            if user['last_day'] is not None:
                last_day = datetime.strptime(user['last_day'], '%d-%m-%Y').date()
                today = date.today() 
                if (today - last_day).days >= 2:
                    db.execute(
                        'UPDATE user'
                        ' SET streak = ?'
                        ' WHERE id = ?',
                        ('0', user['id'])
                    )
                    db.commit()
            return redirect(url_for('index'))
        
        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)

    return wrapped_view
