from flask import Blueprint, render_template, jsonify, request, current_app
from functools import wraps
import jwt
import uuid

from logger.Logger import Logger
from RabbitProducerObject import RabbitProducerObject
from ThreadLockManager import ThreadLockManager


admin = Blueprint("admin", __name__, template_folder="templates")

logger = Logger.get_instance()  # logger
rabbit_producer = RabbitProducerObject('db_requests')  # the que that sends requests to the db from the web server
lock_manager = ThreadLockManager.get_instance()


def admin_token_required(f):
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
            if payload['role'] == 'Administrator':
                return f(*args, **kwargs)

        except (jwt.InvalidTokenError, jwt.ExpiredSignature, jwt.DecodeError, KeyError):
            logger.logger.warning('A user tried to used a function that requires token but token is not valid.')
            return jsonify({'message': 'Token is not valid'}), 401

    return decorated


@admin.route('/')
def home():
    return render_template('admin/home.html')  # react page demo


@admin_token_required
@admin.route('/customers', methods=['GET', 'POST'])  # get all customers, add customer
def customers():
    request_id = str(uuid.uuid4())

    if request.method == 'GET':
        rabbit_producer.publish({'id_': request_id, 'data': 'data'})  # data empty for now
        lock_manager.lock_thread(request_id)
        pass

    elif request.method == 'POST':
        rabbit_producer.publish({'id_': request_id, 'data': 'data'})  # data empty for now
        lock_manager.lock_thread(request_id)
        pass


@admin_token_required
@admin.route('/customers/<int:id_>', methods=['DELETE'])  # delete_customer
def customer_by_id():
    pass


@admin_token_required
@admin.route('/airlines', methods=['POST'])  # add airline
def airlines():
    pass


@admin_token_required
@admin.route('/airlines/<int:id_>', methods=['GET', 'DELETE'])  # get airline by id, delete airline
def airline_by_id():
    pass


@admin_token_required
@admin.route('/admins', methods=['POST'])  # add_admin
def admins():
    pass


@admin_token_required
@admin.route('/admin/<int:id_>', methods=['DELETE'])  # delete_admin
def admin_by_id():
    pass
