import random
import string

from flask import render_template, redirect

from . import app, db
from .models import URLMap
from .forms import URLForm


@app.route('/', methods=['GET', 'POST'])
def get_unique_short_id():
    form = URLForm()
    if form.validate_on_submit():
        if form.custom_id.data == '':
            link_array = ''.join(
                random.choice(
                    string.ascii_letters + string.digits) for _ in range(16)
            )
            short_link = link_array

            new_url = URLMap(
                original=form.original_link.data,
                short=short_link
            )
            db.session.add(new_url)
            db.session.commit()

            new_link = URLMap.query.filter_by(short=short_link).first()
            context = {'form': form, 'short_link': short_link}
            return render_template('index.html', **context)
        else:
            short_link = form.custom_id.data
            new_url = URLMap(
                original=form.original_link.data,
                short=short_link
            )
            db.session.add(new_url)
            db.session.commit()
            context = {'form': form, 'short_link': short_link}
            return render_template('index.html', **context)

    return render_template('index.html', form=form)


@app.route('/<path:short_id>')
def redirect_func(short_id):
    redir_link = URLMap.query.filter_by(short=short_id).first()
    return redirect(redir_link.original)

