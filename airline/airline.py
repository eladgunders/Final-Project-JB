from flask import Blueprint, render_template, jsonify, request, current_app, make_response
from functools import wraps
import jwt
import uuid

from logger.Logger import Logger
from RabbitProducerObject import RabbitProducerObject
from ThreadLockManager import ThreadLockManager


airline = Blueprint("airline", __name__, template_folder="templates")


logger = Logger.get_instance()  # logger
rabbit_producer = RabbitProducerObject('db_requests')  # the que that sends requests to the db from the web server
lock_manager = ThreadLockManager.get_instance()


def airline_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            token = token.removeprefix('Bearer ')

        if not token:
            logger.logger.info('A user tried to used a function that requires token but token is missing.')
            return jsonify({'message': 'Token is missing'}), 401

        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'])
            if payload['role'] == 'Airline Company':
                return f(payload, *args, **kwargs)
            else:
                jsonify({'message': 'Token is not valid'}), 401

        except (jwt.InvalidTokenError, jwt.ExpiredSignature, jwt.DecodeError, KeyError):
            logger.logger.warning('A user tried to used a function that requires token but token is not valid.')
            return jsonify({'message': 'Token is not valid'}), 401

    return decorated


@airline.route('/')
@airline_token_required
def home(login_token):
    return render_template('airline/home.html')


@airline.route('/flights', methods=['GET', 'POST'])
@airline_token_required
def flights(login_token):
    pass


@airline.route('/flights/<int:id_>', methods=['PATCH', 'DELETE'])
@airline_token_required
def flight_by_id(login_token, id_):
    pass


@airline.route('/airlines/<int:id_>', methods=['PATCH'])
@airline_token_required
def airline_by_id(login_token, id_):
    pass
