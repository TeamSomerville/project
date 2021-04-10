from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class UpdateRatingForm(FlaskForm):
    rating = StringField('Rating', validators=[DataRequired()])
    submit = SubmitField('Update')
