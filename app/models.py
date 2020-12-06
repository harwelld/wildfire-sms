from flask_wtf import FlaskForm
from app.includes.utils import isFieldUnique
from wtforms import HiddenField, SubmitField, StringField, SelectField
from wtforms.validators import *


class RegistrationForm(FlaskForm):
    """Registration form model and validation"""

    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    def validate_username(form, field):
        if isFieldUnique(field.data, 'user_name'):
            pass
        else:
            raise ValidationError('Username is already in use, please try another.')

    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=12, max=12, message="Phone number has an invalid length.")])
    def validate_phone(form, field):
        # TODO: regex to validate format ###-###-####
        if isFieldUnique(field.data, 'user_phone'):
            pass
        else:
            raise ValidationError('Phone number is already in use, please try another.')

    distance = SelectField('Notification Distance', choices=[('5','5 miles'),('10','10 miles'),('15','15 miles'),('20','20 miles')], validators=[DataRequired()])

    autocomplete = StringField('Address or nearby location', validators=[DataRequired(message='A valid address or location is required')])

    latitude = HiddenField('Latitude', validators=[DataRequired()])
    def validate_latitude(field, form):
        if field.data == '' or field.data == None:
            raise ValidationError(message='Latitude is empty')

    longitude = HiddenField('Longitude', validators=[DataRequired()])
    def validate_longitude(field, form):
        if field.data == '' or field.data == None:
            raise ValidationError(message='Longitude is empty')

    submit = SubmitField('Register')
