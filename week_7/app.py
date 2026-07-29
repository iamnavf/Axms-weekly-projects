from flask import Flask

app = Flask(__name__)


@app.route('/')
def dashboard():
    pass

@app.route('/diagnosis')
def diagnosis():
    pass

@app.route('/prediction')
def prediction():
    pass

@app.route('/analytics')
def diagnosis():
    pass

@app.route('/report')
def diagnosis():
    pass


if __name__ == '__main__':
    app.run(debug = True)