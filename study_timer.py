from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from datetime import datetime, date

from myproject.auth import login_required
from myproject.db import get_db

bp = Blueprint('study_timer', __name__)


def validate_streak(id):
    db = get_db()
    user = db.execute(
        'SELECT * FROM user'
        ' WHERE id = ?',
        (id,)
    ).fetchone()
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
    if g.user['id'] is not None:
        validate_streak(g.user['id'])
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

    #total_time = db.execute(
    #    'SELECT total_time FROM user '
    #    ' WHERE id = ?',
    #    (g.user['id'],)
    #).fetchone()

    #total_time_hour = int(total_time[:-6]) + int(hours)
    #total_time_minutes = int(total_time[-5:-3]) + int(minutes)
    #total_time_seconds = int(total_time[-2:]) + int(seconds)
    #total_time = str(total_time_hour) + ":" + str(total_time_minutes) + ":" + str(total_time_seconds)

    #db.execute(
    #    'UPDATE user'
    #    ' SET total_time = ?'
    #    ' WHERE id = ?',
    #    (total_time, g.user['id'])
    #)
    #db.commit()

    user_data = db.execute(
            'SELECT * FROM user'
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
            ' streak = ?'
            ' WHERE id = ?',
            (today, current_streak, g.user['id'])
        )
        db.commit()

        #longest_streak = db.execute(
        #    'SELECT longest_streak FROM user'
        #    ' WHERE id = ?',
        #    (g.user['id'],)
        #).fetchone()
        
        #if current_streak > longest_streak:
        #    db.execute(
        #        'UPDATE user'
        #        ' SET longest_streak = ?'
        #        ' WHERE id = ?',
        #        (current_streak, g.user['id'])
        #    )
        #    db.commit()

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


@bp.route('/about')
def about():
    return render_template('study_timer/about.html')