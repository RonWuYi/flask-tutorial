from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    print('during view')
    return 'Hello, World!'


@app.teardown_appcontext
def show_terdown(exception):
    print('after with block')


with app.test_request_context():
    print('during with block')


with app.test_client():
    client.get('/')
    print(request.path)
