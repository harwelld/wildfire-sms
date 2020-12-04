from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import *


class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])

    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=35)])

    distance = SelectField('Notification Distance', choices=[('5', '5 miles'),('10', '10 miles'),('15', '15 miles')], validators=[DataRequired()])

    autocomplete = StringField('Address or nearby location', validators=[DataRequired()])

    submit = SubmitField('Register')