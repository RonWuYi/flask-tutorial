from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from .utilities import *

bp = Blueprint('kms', __name__)

@bp.route('/kms')
def index():
    db  = get_db()
    kms = db.execute(
        # 'SELECT e.id, user_id, created, env_name'
        # ' FROM env e JOIN user u ON e.user_id = u.id'
        # ' ORDER BY created DESC'
        'SELECT * FROM kms WHERE private_device == 1'
    ).fetchall()

    return render_template('kms/index.html', kms=kms)


@bp.route('/kms/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        env_id = request.form.get('env_id')
        kms_user = request.form.get('kms_user')
        kms_password = request.form.get('kms_password')
        kms_ip = request.form.get('kms_ip')
        domain_name = request.form.get('domain_name')
        test_root_folder = request.form.get('test_root_folder')
        branch = request.form.get('branch')
        db_name = request.form.get('db_name')
        db_user = request.form.get('db_user')
        db_password = request.form.get('db_password')
        db_host = request.form.get('db_host')
        db_ip = request.form.get('db_ip')
        sa_name = request.form.get('sa_name')
        sa_password = request.form.get('sa_password')
        private_device = request.form.get('private_device')
        if private_device is None:
            private_device = 0
        error = None

        if not kms_ip:
            error = 'kms is is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
            'INSERT INTO kms (user_id, env_id, kms_user, kms_password, kms_ip, domain_name, test_root_folder, branch, db_name, db_user, db_password, db_host, db_ip, sa_name, sa_password, private_device)'
            ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (g.user['id'], 
             env_id, 
             kms_user, 
             kms_password, 
             kms_ip,
             domain_name,
             test_root_folder,
             branch,
             db_name,
             db_user,
             db_password,
             db_host,
             db_ip,
             sa_name,
             sa_password,
             private_device)
            )
            db.commit()
            return redirect(url_for('kms.index'))

    return render_template('kms/create.html',
                            env=get_empty_vaule(empty_sql.format('env', 'kms_id'))
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

def get_kms(id, check_creator=True):
    kms = get_db().execute(
        'SELECT k.id, env_name, created, user_id'
        ' FROM kms k JOIN user u ON k.user_id = u.id'
        ' WHERE u.id = ?',
        (id,)
    ).fetchone()
    
    if kms is None:
        abort(404, f'Kms id {id} does not exists.')
    if check_creator and kms['user_id'] != g.user['id']:
        abort(403)
        
    return kms

@bp.route('/kms/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    kms = get_kms(id)
    
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
            return redirect(url_for('kms.index'))

    return render_template('kms/update.html', kms=kms)
        
    
@bp.route('/kms/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_kms(id)
    db = get_db()
    db.execute('DELETE FROM kms WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('kms.index'))