import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from myproject.auth import login_required
from myproject.db import get_db

bp = Blueprint('account', __name__, url_prefix='/account')

@bp.route('/change-login', methods=('GET', 'POST'))
@login_required
def change_login():
    db = get_db()
    account_info = db.execute(
        'SELECT * FROM user'
        ' WHERE id = ?',
        (g.user['id'],)
    ).fetchone()
    if request.method == 'GET':
        return render_template('account/change-login.html', account_info=account_info)
    
    elif request.method == 'POST':
        email = request.form['email']
        email_confirm = request.form['email_confirm']
        new_pw = request.form['new_pw']
        new_pw_confirm = request.form['new_pw_confirm']
        old_pw = request.form['old_pw']
        db = get_db()
        error = None

        if not old_pw:
            error = 'Password is required.'

        if email != "" and email != account_info['email']:
            if email != email_confirm:
                error = "The confirmation e-mail doesn't match."
            if db.execute(
                'SELECT id FROM user WHERE email = ?', (email,)
                ).fetchone() is not None:
                error = 'Email {} is already registered.'.format(email)
        
        if email_confirm != "" and email != email_confirm:
            error = "The confirmation e-mail doesn't match."

        if new_pw != "":
            if len(new_pw) < 6 or not any(str.isdigit(c) for c in new_pw) or not any(str.isalpha(c) for c in new_pw):
                error = 'New password must contain at least one number and one letter and must be at least six characters long.'
            elif new_pw != new_pw_confirm:
                error = "The provided passwords don't match."
        
        if error is None:
            if not check_password_hash(account_info['password'], old_pw):
                error = 'Incorrect password.'

        if error is None:
            if new_pw != "":
                db.execute(
                    'UPDATE user'
                    ' SET email = ?,'
                    ' PASSWORD = ?'
                    ' WHERE id = ?',
                    (email, generate_password_hash(new_pw), g.user['id'])
                )
            else:
                db.execute(
                    'UPDATE user'
                    ' SET email = ?'
                    ' WHERE id = ?',
                    (email, g.user['id'])
                )
            db.commit()
            return redirect(url_for('study_timer.account'))
        else:
            flash(error)
            return render_template('account/change-login.html', account_info=account_info)


@bp.route('/save-settings', methods=('POST',))
@login_required
def save_settings():
    username = request.form['account_username']
    weekdays = ""
    dark_mode = 'no'
    if request.form.get('mon') is not None:
        weekdays += 'mon'
    if request.form.get('tue') is not None:
        weekdays += 'tue'
    if request.form.get('wed') is not None:
        weekdays += 'wed'
    if request.form.get('thu') is not None:
        weekdays += 'thu'
    if request.form.get('fri') is not None:
        weekdays += 'fri'
    if request.form.get('sat') is not None:
        weekdays += 'sat'
    if request.form.get('sun') is not None:
        weekdays += 'sun'
    if request.form['account_study_time'].isnumeric():
        goal = int(request.form['account_study_time'])
    else:
        goal = 60

    if request.form.get('dark_mode') is not None:
        dark_mode = 'yes'

    error = None
    db = get_db()
    user_id = g.user['id']
    if len(username) < 6 or len(username) > 15:
        error = 'Username must be between 6 and 15 characters.'
    elif goal < 1 or goal > 1440:
        error = 'Invalid study goal time.'
    elif username != g.user['username'] and db.execute(
        'SELECT * from user'
        ' WHERE username = ?',
        (username,)
    ).fetchone() is not None:
        error = 'This username is already in use.'
    else:
        db.execute(
            'UPDATE user'
            ' SET username = ?,'
            ' min_study_time = ?,'
            ' weekdays = ?,'
            ' dark_mode = ?'
            ' WHERE id = ?',
            (username, goal, weekdays, dark_mode, user_id)
        )
        db.commit()
    if error is not None:
        flash(error)
    return redirect(url_for('study_timer.account'))