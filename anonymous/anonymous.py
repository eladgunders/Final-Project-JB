from flask import Blueprint, render_template

anonymous = Blueprint("anonymous", __name__, template_folder="templates")


@anonymous.route("/")
def home():
    return render_template('anonymous/home.html')