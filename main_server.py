from flask import Flask, render_template, session, jsonify
from flask_cors import CORS
from anonymous.anonymous import anonymous
from admin.admin import admin


app = Flask(__name__)

app.register_blueprint(anonymous, url_prefix="/anonymous")
app.register_blueprint(admin, url_prefix="/admin")

CORS(app)


@app.route("/")
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)