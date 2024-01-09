import random
import string

from flask import render_template, redirect, flash

from . import app, db
from .error_handler import InvalidAPIUsage
from .forms import URLForm
from .models import URLMap
from .constants import (LENGTH_LINK, STATUS_CODE_NOT_FOUND)


def create_random_short_url():
    link_array = ''.join(
        random.choice(
            string.ascii_letters + string.digits
        ) for _ in range(LENGTH_LINK)
    )
    return link_array


@app.route('/', methods=['GET', 'POST'])
def get_unique_short_id():
    form = URLForm()
    if form.validate_on_submit():
        if form.custom_id.data in [None, '']:
            new_short_url = create_random_short_url()
            new_url = URLMap(
                original=form.original_link.data,
                short=new_short_url
            )
            db.session.add(new_url)
            db.session.commit()
            flash(new_short_url)
            context = {'form': form, 'short_link': new_short_url}
            return render_template('content.html', **context)
        else:
            short_url = form.custom_id.data
            if URLMap.query.filter_by(short=short_url).first():
                flash('Предложенный вариант короткой ссылки уже существует.')
                return render_template('content.html', form=form)
            new_url = URLMap(
                original=form.original_link.data,
                short=short_url
            )
            db.session.add(new_url)
            db.session.commit()
            flash(short_url)
            context = {'form': form, 'short_link': short_url}
            return render_template('content.html', **context)

    return render_template('content.html', form=form)


@app.route('/<string:short_id>', methods=['GET'])
def redirect_func(short_id):
    redirect_link = URLMap.query.filter_by(short=short_id).first()
    if redirect_link is None:
        raise InvalidAPIUsage('Данный url не найден', STATUS_CODE_NOT_FOUND)
    return redirect(redirect_link.original)

