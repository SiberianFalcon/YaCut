from random import choice

from flask import render_template, redirect, flash, url_for

from . import app, db
from .constants import (
    CREATE_RANDOM_LINK, STATUS_CODE_NOT_FOUND, LENGTH_LINK
)
from .error_handler import InvalidAPIUsage
from .forms import URLForm
from .models import URLMap


def create_random_short_url():
    while True:
        random_link = ''.join(
            choice(CREATE_RANDOM_LINK) for _ in range(LENGTH_LINK))

        if not URLMap.query.filter_by(short=random_link).first():
            return random_link


def add_to_database(url, short_link=None):
    if short_link is None:
        short_link = create_random_short_url()
    model = URLMap(
        original=url,
        short=short_link
    )
    db.session.add(model)
    db.session.commit()

    flash(
        url_for(
            'get_unique_short_id',
            _scheme='http',
            _external=True
        )
        + short_link
    )


@app.route('/', methods=['GET', 'POST'])
def get_unique_short_id():
    form = URLForm()
    if form.validate_on_submit():
        if not form.custom_id.data:
            add_to_database(form.original_link.data)
            return render_template('content.html', form=form)

        new_short_url = form.custom_id.data
        if URLMap.query.filter_by(short=new_short_url).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('content.html', form=form)
        add_to_database(form.original_link.data, new_short_url)
        return render_template('content.html', form=form)
    return render_template('content.html', form=form)


@app.route('/<string:short_id>', strict_slashes=False)
def redirect_func(short_id):
    return redirect(
        URLMap.query.filter_by(short=short_id).first_or_404().original,
    )
