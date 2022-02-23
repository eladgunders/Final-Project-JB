from flask import Flask, render_template
from facades.AnonymousFacade import AnonymousFacade
from data_access_objects.DbRepoPool import DbRepoPool
import json

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/myname")
def my_name():
    return render_template('my_name.html')


@app.route("/getpower/<int:num>", methods=['GET'])
def get_power(num):
    return str(num**2)


@app.route("/flights", methods=['GET'])
def get_all_flights():
    repool = DbRepoPool.get_instance()
    repo = repool.get_connection()
    anonfcade = AnonymousFacade(repo)
    all_flights = anonfcade.get_all_flights()
    return json.dumps(all_flights)

if __name__ == '__main__':
    app.run()