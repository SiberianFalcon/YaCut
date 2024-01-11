from random import choice

from flask import render_template, redirect, flash

from . import app, db
from .constants import (
    CREATE_RANDOM_LINK, STATUS_CODE_NOT_FOUND, LENGTH_LINK)
from .error_handler import InvalidAPIUsage
from .forms import URLForm
from .models import URLMap


def add_to_database(url, short_link):
    model = URLMap(
        original=url,
        short=short_link
    )
    db.session.add(model)
    db.session.commit()


def create_random_short_url():
    while True:
        random_link = ''.join(
            choice(CREATE_RANDOM_LINK) for _ in range(LENGTH_LINK))

        if not URLMap.query.filter_by(short=random_link).first():
            return random_link


@app.route('/', methods=['GET', 'POST'])
def get_unique_short_id():
    form = URLForm()
    if form.validate_on_submit():
        if not form.custom_id.data:
            new_short_url = create_random_short_url()
            add_to_database(form.original_link.data, new_short_url)
            flash(new_short_url)
            context = {'form': form, 'short_link': new_short_url}
            return render_template('content.html', **context)

        new_short_url = form.custom_id.data
        if URLMap.query.filter_by(short=new_short_url).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('content.html', form=form)
        add_to_database(form.original_link.data, new_short_url)
        flash(new_short_url)
        context = {'form': form, 'short_link': new_short_url}
        return render_template('content.html', **context)

    return render_template('content.html', form=form)


@app.route('/<string:short_id>', methods=['GET'])
def redirect_func(short_id):
    redirect_link = URLMap.query.filter_by(short=short_id).first()
    if not redirect_link:
        raise InvalidAPIUsage('Данный url не найден', STATUS_CODE_NOT_FOUND)
    return redirect(redirect_link.original)
