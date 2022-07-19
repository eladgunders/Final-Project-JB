from flask import Flask, render_template, session, jsonify
from flask_cors import CORS
from anonymous.anonymous import anonymous
from admin.admin import admin


app = Flask(__name__)

app.register_blueprint(anonymous, url_prefix="/anonymous")
app.register_blueprint(admin, url_prefix="/admin")
app.config['SECRET_KEY']: str = 'SHHH KEEP IT SECRET'  # for the jwt encoding
app.config['threads_locks_dict']: dict = {}  # for managing the requests from the different threads

CORS(app)


@app.route("/")
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
