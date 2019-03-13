import os
from flask import (Blueprint, flash, g, redirect, render_template,request, url_for)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from flaskr.db import get_db

UPLOAD_FOLDER = '/tmp/uploadfiles'
ALLOWED_EXTENSIONS = set(['txt', 'jpg', 'jpeg', 'png'])

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
    name_list = []
    cur_list1 = db.execute('select * from files').fetchall()
    # cur_list2 = db.execute('select * from files').fetchone()
    # for i in list:
    #     print(i)
    for a, b, c, d, e in cur_list1:
        name_list.append(b)
    return 'this is a test page list {}'.format(name_list)


@bp.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    # x, y, z = os.walk(UPLOAD_FOLDER)
    if request.method == 'POST':
        db = get_db()
        error = None
        if 'file' not in request.files:
            error = 'No file part'
            flash(error)
            return redirect(request.url)
        select_files = request.files.getlist('file')
        dup_file_lists = []
        new_file_lists = []
        for f in select_files:
            if f.filename == '':
                error = 'No seleted file'
                flash(error)
                return redirect(request.url)
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                if os.path.exists(UPLOAD_FOLDER):

                    # Todo "not finished yet"
                    if os.path.isfile(os.path.join(UPLOAD_FOLDER, filename)):
                        # return redirect('/')
                        dup_file_lists.append(filename)
                        # flash('{} will be covered'.format(filename))
                        f.save(os.path.join(UPLOAD_FOLDER, filename))
                    else:
                        new_file_lists.append(filename)
                        f.save(os.path.join(UPLOAD_FOLDER, filename))
                   # f.save(os.path.join(UPLOAD_FOLDER, filename))
                else:
                    os.makedirs(UPLOAD_FOLDER)
                    f.save(os.path.join(UPLOAD_FOLDER, filename))
            else:
                flash('some files not allowed to upload, upload process cancelled')

        if len(dup_file_lists) > 0:
            for i in dup_file_lists:
            #     db.execute(
            #         'UPDATE files ()'
            #     )
                try:
                    db.execute(
                        'INSERT INTO files (file_name, checked, strong) VALUES (?, ?, ?)',
                        (i, 0, None)
                    )
                    db.commit()
                except db.Error as e:
                    print(e)
            flash('those dup files {} already overwrite'.format(dup_file_lists))
        db.commit()
        if len(new_file_lists) > 0:
            for i in new_file_lists:
                try:
                    db.execute(
                        'INSERT INTO files (file_name, checked, strong) VALUES (?, ?, ?)',
                        (i, 0, None)
                    )
                    db.commit()
                except db.Error as e:
                    print(e)
            flash('those new files {} already uploaded'.format(new_file_lists))

        return redirect(url_for('upload.upload_file'))
    else:
        new_files = os.listdir(UPLOAD_FOLDER)
        return render_template('/up/up.html', new_files=new_files)

    # return '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form method=post enctype=multipart/form-data>
    #     <input type=file name=file multiple>
    #     <input type=submit value=Upload>
    # </form>
    # <ul>
    # {% for file in new_files %}
    #     <li><a href='/'>{{ file.filename }}</li>
    # {% endfor %}
    # </ul>
    # '''
    # new_files = os.listdir(UPLOAD_FOLDER)
    # return render_template('/up/up.html', new_files=new_files)
