from string import ascii_letters, digits

from flask import jsonify, request, url_for

from . import app, db
from .constants import (
    MAX_CUSTOM_LINK_LENGTH, FORBIDDEN_EXPRESSIONS,
    STATUS_CODE_OK, STATUS_CODE_CREATED, STATUS_CODE_NOT_FOUND
)
from .error_handler import InvalidAPIUsage
from .models import URLMap
from .views import create_random_short_url


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()

    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data or data['url'] == '':
        raise InvalidAPIUsage('"url" является обязательным полем!')

    if 'custom_id' not in data or not data['custom_id']:
        new_short_url = create_random_short_url()
        new_link = URLMap(
            original=data['url'],
            short=new_short_url
        )
        db.session.add(new_link)
        db.session.commit()
        return (jsonify({
            'url': data['url'],
            'short_link': url_for(
                endpoint='get_unique_short_id',
                _external=True,
                _scheme='http') + new_short_url}),
                STATUS_CODE_CREATED)

    if URLMap.query.filter_by(short=data['custom_id']).first():
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.')

    if (data['custom_id'] not in [ascii_letters, digits]
            or data['custom_id'] in FORBIDDEN_EXPRESSIONS
            or len(data['custom_id']) > MAX_CUSTOM_LINK_LENGTH):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    new_link = URLMap(
        original=data['url'],
        short=data['custom_id']
    )
    db.session.add(new_link)
    db.session.commit()
    return (jsonify(
        {
            'url': data['url'],
            'short_link': f"http://localhost/{data['custom_id']}"}),
            STATUS_CODE_CREATED
            )


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    short_link = URLMap.query.filter_by(short=short_id).first()
    if short_link is None:
        return jsonify(
            {'message': 'Указанный id не найден'}
        ), STATUS_CODE_NOT_FOUND

    return jsonify({'url': short_link.original}), STATUS_CODE_OK
