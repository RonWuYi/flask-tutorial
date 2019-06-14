import os
from flask import Flask, flash, request, url_for, redirect, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp/uploadfiles'
# ALLOWED_EXTENSIONS = set(['txt', 'jpg', 'jpeg', 'png'])
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py', silent=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
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
                if os.path.exists(app.config['UPLOAD_FOLDER']):
                    if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                        pass
                    else:
                        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                else:
                    try:
                        os.makedirs(app.config['UPLOAD_FOLDER'])
                    except OSError:
                        pass
                    if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                        pass
                    else:
                        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                # return redirect(request.url)
                return "cannot upload this file"
        return redirect(url_for('upload_file',
                        filename=filename))
    return render_template("upload/upload.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

