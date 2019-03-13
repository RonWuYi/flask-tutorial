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
    return 'this is a upload test page'


@bp.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        select_files = request.files.getlist('file')
        for f in select_files:
            if f.filename == '':
                flash('No seleted file')
                return redirect(request.url)
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                if os.path.exists(UPLOAD_FOLDER):
                    # Todo "not finished yet"
                    if os.path.isfile(os.path.join(UPLOAD_FOLDER, filename)):
                        f.save(os.path.join(UPLOAD_FOLDER, filename))
                    else:
                        pass
                        
                else:
                    os.makedirs(UPLOAD_FOLDER)
                    f.save(os.path.join(UPLOAD_FOLDER, filename))
        return redirect(url_for('upload.upload_file',
                        filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file multiple>
        <input type=submit value=Upload>
    </form>
    '''
