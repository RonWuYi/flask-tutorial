from functools import wraps
from urllib.parse import urlencode, quote, unquote
from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)


def confirmation_required(desc_fn):
    def inner(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if request.args.get('confirm') != '1':
                desc = desc_fn()
                return redirect(url_for('confirm',
                    desc=desc, action_url=quote(request.url)))
            # else:
            #     return redirect(url_for('cancelled'))
            return f(*args, **kwargs)
        return wrapper
    return inner


@app.route('/confirm')
def confirm():
    desc = request.args['desc']
    action_url = unquote(request.args['action_url'])

    return render_template('_confirm.html', desc=desc, action_url=action_url)


def you_sure():
    return "Are you sure?"


@app.route('/')
@confirmation_required(you_sure)
def hello_world():
    return 'Hello World!'


# @app.route('/cancelled')
# @confirmation_required(you_sure)
# def cancelled():
#     return 'action cancelled'


if __name__ == '__main__':
    app.run(debug=True)
