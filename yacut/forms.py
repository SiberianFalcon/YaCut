from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (
    MAX_FORM_LENGTH_URL, MAX_FORM_LENGTH_ID, MIN_FORM_LENGTH, REGEX
)


class URLForm(FlaskForm):
    original_link = URLField(
        'Введите длинную ссылку',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(MIN_FORM_LENGTH, MAX_FORM_LENGTH_URL)]
    )
    custom_id = StringField(
        'Введите короткую ссылку',
        validators=[
            Optional(),
            Length(MIN_FORM_LENGTH, MAX_FORM_LENGTH_ID),
            Regexp(REGEX)]
    )
    submit = SubmitField('Создать')
