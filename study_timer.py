from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from myproject.auth import login_required
from myproject.db import get_db

bp = Blueprint('study_timer', __name__)

@bp.route('/')
def index():
    return render_template('study_timer/index2.html')


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
    return redirect(url_for('study_timer.index'))
