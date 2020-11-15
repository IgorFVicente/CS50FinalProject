from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from datetime import date

from myproject.auth import login_required
from myproject.db import get_db

bp = Blueprint('study_timer', __name__)

def validate_goal(id):
    db = get_db()
    user_data = db.execute(
        'SELECT * FROM user'
        ' WHERE id = ?',
        (id,)
    ).fetchone()
    min_time = user_data['min_study_time']
    db = get_db()
    today = date.today()
    today = today.strftime("%d/%m/%Y")
    timer_history = db.execute(
        'SELECT r.id, created, hours, minutes, seconds, user_id'
        ' FROM records r JOIN user u ON r.user_id = u.id'
        ' WHERE u.id = ? AND created = ? ORDER BY created DESC',
        (id, today)
    ).fetchall()
    today_sum = 0
    for history in timer_history:
        today_sum += history['hours'] * 60
        today_sum += history['minutes']
        today_sum += history['seconds'] / 60
    if today_sum >= min_time:
        return True
    else:
        return False


@bp.route('/')
def index():
    return render_template('study_timer/index.html')


@bp.route('/history')
@login_required
def history():
    db = get_db()
    timer_history = db.execute(
        'SELECT r.id, created, hours, minutes, seconds, user_id'
        ' FROM records r JOIN user u ON r.user_id = u.id'
        ' WHERE u.id = ? ORDER BY created DESC',
        (g.user['id'],)
    ).fetchall()
    return render_template('study_timer/history.html', timer_history=timer_history)


@bp.route('/save', methods=('POST',))
@login_required
def save():
    timer = str(request.form['timer_repeat'])
    seconds = timer[-2:]
    minutes = timer[-5:-3]
    hours = timer[:-6]
    db = get_db()
    db.execute(
        'INSERT INTO records (hours, minutes, seconds, user_id)'
        ' VALUES (?, ?, ?, ?)',
        (hours, minutes, seconds, g.user['id'])
    )
    db.commit()
    if validate_goal(g.user['id']):
        user_data = db.execute(
            'SELECT * FROM user '
            ' WHERE id = ?',
            (g.user['id'],)
        ).fetchone()
        streak = user_data['streak']
        db.execute(
            'UPDATE user'
            ' SET streak = ?'
            ' WHERE id = ?',
            (streak + 1, g.user['id'])
        )
        db.commit()
    return redirect(url_for('study_timer.index'))


@bp.route('/account', methods=('GET', 'POST'))
@login_required
def account():
    db = get_db()
    account_info = db.execute(
        'SELECT username, min_study_time, streak FROM user'
        ' WHERE id = ?',
        (g.user['id'],)
    ).fetchone()
    return render_template('account/account.html', account_info=account_info)


@bp.route('/tips')
def tips():
    return render_template('study_timer/tips.html')


@bp.route('/about')
def about():
    return render_template('study_timer/about.html')