from flask import (Blueprint, flash, g, redirect, render_template,request, url_for)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db


up = Blueprint('upload', __name__)


@up.route('/upload')
@login_required
def upload():
    return 'this is a upoad page'
