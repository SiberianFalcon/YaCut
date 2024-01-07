import random
import string

from flask import render_template, redirect, flash

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
            context = {'form': form, 'short_link': short_link}
            return render_template('content.html', **context)
        else:
            short_link = form.custom_id.data
            if URLMap.query.filter_by(short=short_link).first():
                flash('Придумайте другое название')
                return render_template('content.html', form=form)
            new_url = URLMap(
                original=form.original_link.data,
                short=short_link
            )
            db.session.add(new_url)
            db.session.commit()
            context = {'form': form, 'short_link': short_link}
            return render_template('content.html', **context)

    return render_template('content.html', form=form)


@app.route('/<path:short_id>')
def redirect_func(short_id):
    redirect_link = URLMap.query.filter_by(short=short_id).first()
    return redirect(redirect_link.original)

