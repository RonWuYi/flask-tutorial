from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from .utilities import devices, devices_sql

bp = Blueprint('env', __name__)

@bp.route('/env')
def index():
    db  = get_db()
    envs = db.execute(
        'SELECT e.id, user_id, created, env_name'
        ' FROM env e JOIN user u ON e.user_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('envs/index.html', envs=envs)


@bp.route('/env/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        envname = request.form.get('envname')
        kms_id = request.form.get('kms_id')
        agent_id = request.form.get('agent_id')
        itms_id = request.form.get('itms_id')
        priority_level = request.form.get('priority_level')

        # iks_id = request.form.get('iks_id')
        # pes_id = request.form.get('pes_id')
        # ccis_id = request.form.get('ccis_id')
        # pg_id = request.form.get('pg_id')

        error = None

        if not envname:
            error = 'envname is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                # 'INSERT INTO env (user_id, env_name, kms_id, agent_id, itms_id, iks_id, pes_id, ccis_id, pg_id, priority_level)'
                'INSERT INTO env (user_id, env_name, kms_id, agent_id, itms_id, priority_level)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (g.user['id'], 
                 envname, 
                 kms_id, 
                 agent_id, 
                 itms_id, 
                #  iks_id, 
                #  pes_id, 
                #  ccis_id, 
                #  pg_id, 
                 priority_level)
            )
            db.commit()
            return redirect(url_for('env.index'))

    return render_template('envs/create.html', 
                            kms=devices(devices_sql.format('kms')), 
                            agent=devices(devices_sql.format('agent')), 
                            itms=devices(devices_sql.format('itms'))
                            # iks=devices(devices_sql.format('iks')), 
                            # pes=devices(devices_sql.format('pes')),
                            # ccis=devices(devices_sql.format('ccis')), 
                            # pg=devices(devices_sql.format('pg'))
                            )

# def get_post(id, check_author=True):
#     post = get_db().execute(
#         'SELECT p.id, title, body, created, author_id, username'
#         ' FROM post p JOIN user u ON p.author_id = u.id'
#         ' WHERE p.id = ?',
#         (id,)
#     ).fetchone()

#     if post is None:
#         abort(404, f'Post id {id} does not exists.')

#     if check_author and post['author_id'] != g.user['id']:
#         abort(403)
        
#     return post

def get_env(id, check_creator=True):
    env = get_db().execute(
        'SELECT e.id, env_name, created, user_id'
        ' FROM env e JOIN user u ON e.user_id = u.id'
        ' WHERE e.id = ?',
        (id,)
    ).fetchone()
    
    if env is None:
        abort(404, f'Env id {id} does not exists.')
    if check_creator and env['user_id'] != g.user['id']:
        abort(403)
        
    return env

@bp.route('/env/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    env = get_env(id)
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        
        error = None
        
        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post set title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('envs/update.html', env=env)
        
    
@bp.route('/env/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_env(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('env.index'))