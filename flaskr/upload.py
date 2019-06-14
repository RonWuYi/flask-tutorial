import os

from flask import (Blueprint, flash, redirect, render_template, request, url_for)
from werkzeug.utils import secure_filename
from flaskr.db import get_db
from pathlib import Path
from . import const

if const.in_linux():
    if os.path.exists('/tmp/uploadfiles'):
        pass
    else:
        os.makedirs('/tmp/uploadfiles')
    UPLOAD_FOLDER = '/tmp/uploadfiles'
else:
    if os.path.exists(os.path.join(str(Path.cwd()), 'uploadfiles')):
        pass
    else:
        os.makedirs(os.path.join(str(Path.cwd()), 'uploadfiles'))
    UPLOAD_FOLDER = os.path.join(str(Path.cwd()), 'uploadfiles')

ALLOWED_EXTENSIONS = {'txt', 'jpg', 'jpeg', 'png'}

bp = Blueprint('upload', __name__, url_prefix='/upload')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/')
def index():
    return 'this is a upload index page'


@bp.route('/test')
def test():
    db = get_db()
    cur_list1 = db.execute('select * from files').fetchall()
    return render_template('/up/table.html', items=cur_list1)


@bp.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        db = get_db()
        error = None
        if 'file' not in request.files:
            error = 'No seleted file'
            flash(error)
            return redirect(request.url)
        select_files = request.files.getlist('file')
        dup_file_lists = []
        new_file_lists = []
        for f in select_files:
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                if os.path.exists(UPLOAD_FOLDER):
                    if os.path.isfile(os.path.join(UPLOAD_FOLDER, filename)):
                        dup_file_lists.append(filename)
                        f.save(os.path.join(UPLOAD_FOLDER, filename))
                    else:
                        new_file_lists.append(filename)
                        f.save(os.path.join(UPLOAD_FOLDER, filename))
                else:
                    os.makedirs(UPLOAD_FOLDER)
                    f.save(os.path.join(UPLOAD_FOLDER, filename))
            else:
                flash('some files not allowed to upload, upload process cancelled')
        if len(dup_file_lists) > 0:
            flash('those dup files {} already overwrite'.format(dup_file_lists))
        if len(new_file_lists) > 0:
            for i in new_file_lists:
                try:
                    db.execute(
                        'INSERT INTO files (file_name, file_path, checked, strong) VALUES (?, ?, ?, ?)',
                        (i, os.path.join(UPLOAD_FOLDER, i), 0, None)
                    )
                    db.commit()
                except db.Error as e:
                    print(e)
            flash('those new files {} already uploaded'.format(new_file_lists))
        cur_list2 = db.execute('select * from files').fetchall()
        return render_template('/up/up.html', items=cur_list2)
        # return redirect(url_for('upload.upload_file'))
    else:
        try:
            new_files = os.listdir(UPLOAD_FOLDER)
            return render_template('/up/up.html', new_files=new_files)
        except FileNotFoundError as e:
            flash(e)
            return render_template('/up/up.html', new_files=None)
