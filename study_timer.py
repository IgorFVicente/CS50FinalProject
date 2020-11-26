from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from datetime import datetime, date, timedelta

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
                weekdays = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
                valid_weekdays = user['weekdays']
                failed_days = 0
                while last_day != date.today():
                    last_day += timedelta(days = 1)
                    if weekdays[last_day.weekday()] in valid_weekdays:
                        failed_days += 1
                if failed_days >= 2:
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
    if g.user is not None:
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

    total_time = db.execute(
        'SELECT * FROM user '
        ' WHERE id = ?',
        (g.user['id'],)
    ).fetchone()['total_time']
    total_time_seconds = int(total_time[-2:])
    total_time_minutes = int(total_time[-5:-3])
    total_time_hours = int(total_time[:-6])

    total_time_seconds += int(seconds)
    if total_time_seconds >= 60:
        total_time_minutes += total_time_seconds // 60
        total_time_seconds = total_time_seconds % 60
    
    total_time_minutes += int(minutes)
    if total_time_minutes >= 60:
        total_time_hours += total_time_minutes // 60
        total_time_minutes = total_time_minutes % 60

    total_time_hours += int(hours)

    counter = 0
    new_time = ""
    for i in (total_time_hours, total_time_minutes, total_time_seconds):
        if i == 0:
            i = '00'
        elif i < 10:
            i = '0' + str(i)
        else:
            i = str(i)
        new_time += i
        counter += 1
        if counter != 3:
          new_time += ':'
    
    db.execute(
        'UPDATE user'
        ' SET total_time = ?'
        ' WHERE id = ?',
        (new_time, g.user['id'])
    )
    db.commit()

    user_data = db.execute(
            'SELECT * FROM user'
            ' WHERE id = ?',
            (g.user['id'],)
        ).fetchone()

    today = date.today()
    today = today.strftime('%d-%m-%Y')
    current_streak = int(user_data['streak'])
    if validate_goal(g.user['id']) and user_data['last_day'] != today:
        new_streak = current_streak + 1
        db.execute(
            'UPDATE user'
            ' SET last_day = ?,'
            ' streak = ?'
            ' WHERE id = ?',
            (today, new_streak, g.user['id'])
        )
        db.commit()

        longest_streak = user_data['longest_streak']
        
        if new_streak > longest_streak:
            db.execute(
                'UPDATE user'
                ' SET longest_streak = ?'
                ' WHERE id = ?',
                (new_streak, g.user['id'])
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
    weekdays = account_info['weekdays']
    return render_template('account/account.html', account_info=account_info, weekdays=weekdays)


@bp.route('/about')
def about():
    return render_template('study_timer/about.html')