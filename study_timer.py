from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
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
    today = today.strftime('%Y-%m-%d')
    timer_history = db.execute(
        'SELECT id, created, created_date, created_time, hours, minutes, seconds, user_id'
        ' FROM records'
        ' WHERE user_id = ? AND created_date = ? ORDER BY created DESC',
        (id, today)
    ).fetchall()

    today_sum = 0
    for history in timer_history:
        today_sum += int(history['hours']) * 60
        today_sum += int(history['minutes'])
        today_sum += int(history['seconds']) / 60    
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
    user_data = db.execute(
        'SELECT * FROM user'
        ' WHERE id = ?',
        (g.user['id'],)
    ).fetchone()
    timer_history = db.execute(
        'SELECT r.id, created, created_date, created_time, hours, minutes, seconds, user_id'
        ' FROM records r JOIN user u ON r.user_id = u.id'
        ' WHERE u.id = ? ORDER BY created DESC',
        (g.user['id'],)
    ).fetchall()
    return render_template('study_timer/history.html', timer_history=timer_history, user_data=user_data)


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

    user_data = db.execute(
            'SELECT * FROM user '
            ' WHERE id = ?',
            (g.user['id'],)
        ).fetchone()

    today = date.today()
    today = today.strftime('%d-%m-%Y')
    if validate_goal(g.user['id']) and user_data['last_day'] != today:
        current_streak = str(int(user_data['streak']) + 1)
        db.execute(
            'UPDATE user'
            ' SET last_day = ?,'
            ' streak = ?',
            (today, current_streak)
        )
        db.commit()
    return redirect(url_for('study_timer.index'))


@bp.route('/account', methods=('GET', 'POST'))
@login_required
def account():
    db = get_db()
    account_info = db.execute(
        'SELECT * FROM user'
        ' WHERE id = ?',
        (g.user['id'],)
    ).fetchone()
    c = 0
    weekdays = []
    #while c < len(account_info['weekdays']):
    #    weekdays.append(account_info['weekdays'][c:c+3])
    #    c += 3
    weekdays = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    return render_template('account/account.html', account_info=account_info, weekdays=weekdays)


@bp.route('/tips')
def tips():
    return render_template('study_timer/tips.html')


@bp.route('/about')
def about():
    return render_template('study_timer/about.html')