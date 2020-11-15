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
        'SELECT email FROM user'
        ' WHERE id = ?',
        (g.user['id'],)
    ).fetchone()
    if request.method == 'GET':
        return render_template('account/change-login.html', account_info=account_info)
    
    elif request.method == 'POST':
        return render_template('account/change-login.html')


@bp.route('/save-settings', methods=('POST',))
@login_required
def save_settings():
    username = request.form['account_username']
    min_study_time = request.form['account_study_time']
    db = get_db()
    user_id = g.user['id']
    db.execute(
        'UPDATE user'
        ' SET username = ?,'
        ' min_study_time = ?'
        ' WHERE id = ?',
        (username, min_study_time, user_id)
    )
    db.commit()
    return redirect(url_for('study_timer.account'))