from flask import Blueprint, render_template, jsonify, request, current_app, make_response
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
                return f(payload, *args, **kwargs)
            else:
                jsonify({'message': 'Token is not valid'}), 401

        except (jwt.InvalidTokenError, jwt.ExpiredSignature, jwt.DecodeError, KeyError):
            logger.logger.warning('A user tried to used a function that requires token but token is not valid.')
            return jsonify({'message': 'Token is not valid'}), 401

    return decorated


@admin.route('/')
@admin_token_required
def home(login_token):
    return render_template('admin/home.html')  # react page demo


@admin.route('/customers', methods=['GET', 'POST'])  # get all customers, add customer
@admin_token_required
def customers(login_token):
    request_id: str = str(uuid.uuid4())

    if request.method == 'GET':
        rabbit_producer.publish({'id_': request_id, 'login_token': login_token, 'method': 'get',
                                 'resource': 'customer'})
        lock_manager.lock_thread(request_id)  # acquiring the thread
        # after release getting the answer from app.config by the request id:
        answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
        return make_response(jsonify(answer_from_core), answer_from_core['status'])

    elif request.method == 'POST':
        new_customer: dict = request.get_json()
        rabbit_producer.publish({'id_': request_id, 'login_token': login_token, 'method': 'post',
                                 'resource': 'customer', 'data': new_customer})
        lock_manager.lock_thread(request_id)
        answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
        return make_response(jsonify(answer_from_core), answer_from_core['status'])


@admin.route('/customers/<int:id_>', methods=['DELETE'])  # delete_customer
@admin_token_required
def customer_by_id(login_token, id_):
    request_id: str = str(uuid.uuid4())

    if request.method == 'DELETE':
        rabbit_producer.publish({'id_': request_id, 'login_token': login_token, 'method': 'delete',
                                 'resource': 'customer', 'resource_id': id_})
        lock_manager.lock_thread(request_id)
        answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
        return make_response(jsonify(answer_from_core), answer_from_core['status'])


@admin.route('/airlines', methods=['POST'])  # add airline
@admin_token_required
def airlines(login_token):
    request_id: str = str(uuid.uuid4())

    if request.method == 'POST':
        new_airline: dict = request.get_json()
        rabbit_producer.publish({'id_': request_id, 'login_token': login_token, 'method': 'post',
                                 'resource': 'airline', 'data': new_airline})
        lock_manager.lock_thread(request_id)
        answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
        return make_response(jsonify(answer_from_core), answer_from_core['status'])


@admin.route('/airlines/<int:id_>', methods=['DELETE'])  # delete airline
@admin_token_required
def airline_by_id(login_token, id_):
    request_id: str = str(uuid.uuid4())

    if request.method == 'DELETE':
        rabbit_producer.publish({'id_': request_id, 'login_token': login_token, 'method': 'delete',
                                 'resource': 'airline', 'resource_id': id_})
        lock_manager.lock_thread(request_id)
        answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
        return make_response(jsonify(answer_from_core), answer_from_core['status'])


@admin.route('/admins', methods=['POST'])  # add_admin
@admin_token_required
def admins(login_token):
    request_id: str = str(uuid.uuid4())

    if request.method == 'POST':
        new_admin: dict = request.get_json()
        rabbit_producer.publish({'id_': request_id, 'login_token': login_token, 'method': 'post',
                                 'resource': 'admin', 'data': new_admin})
        lock_manager.lock_thread(request_id)
        answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
        return make_response(jsonify(answer_from_core), answer_from_core['status'])


@admin.route('/admin/<int:id_>', methods=['DELETE'])  # delete_admin
@admin_token_required
def admin_by_id(login_token, id_):
    request_id: str = str(uuid.uuid4())

    if request.method == 'DELETE':
        rabbit_producer.publish({'id_': request_id, 'login_token': login_token, 'method': 'delete',
                                 'resource': 'admin', 'resource_id': id_})
        lock_manager.lock_thread(request_id)
        answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
        return make_response(jsonify(answer_from_core), answer_from_core['status'])
