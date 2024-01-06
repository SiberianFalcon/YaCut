import random
import string

from flask import render_template

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
            short_link = f'http://127.0.0.1:5000/{link_array}'

            new_url = URLMap(
                original=form.original_link.data,
                short=short_link
            )
            db.session.add(new_url)
            db.session.commit()

            new_link = URLMap.query.filter_by(short=short_link).first()
            context = {'form': form, 'new_link': new_link}
            return render_template('index.html', form=form)
        else:
            short_link = f'http://127.0.0.1:5000/{form.custom_id.data}'
            new_url = URLMap(
                original=form.original_link.data,
                short=short_link
            )
            db.session.add(new_url)
            db.session.commit()
            # context = {'form': form, 'new_link': form.custom_id.data}
            return render_template('index.html', form=form)

    return render_template('index.html', form=form)
