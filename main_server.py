from flask import Flask, render_template, session, jsonify
from flask_cors import CORS
from airline.airline import airline
from admin.admin import admin
from customer.customer import customer


app = Flask(__name__)

app.register_blueprint(customer, url_prefix="/customer")
app.register_blueprint(airline, url_prefix="/airline")
app.register_blueprint(admin, url_prefix="/admin")

app.config['SECRET_KEY']: str = 'SHHH KEEP IT SECRET'  # for the jwt encoding

CORS(app)


@app.route("/")
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
