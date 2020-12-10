# -----------------------------------------------------------------------------
# Name:        models.py
#
# Purpose:     Registration form model and validation
#
# Author:      Dylan Harwell - UW Madison
#
# Created:     12/01/2020
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm
from app.includes.utils import isFieldUnique
from wtforms import HiddenField, SubmitField, StringField, SelectField
from wtforms.validators import *


class RegistrationForm(FlaskForm):
    """Registration form model and server-side validation"""

    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    def validate_username(form, field):
        if isFieldUnique(field.data, 'user_name'):
            pass
        else:
            raise ValidationError('Username is already in use, please try another.')

    phone = StringField('Mobile Phone Number', validators=[DataRequired(), Length(min=12, max=12, message='Phone number has an invalid length.')])
    def validate_phone(form, field):
        # TODO: python regex to validate format ###-###-####
        # JS input validator disables all keys except numeric, but Shift+numeric chars still work
        strippedPhone = field.data.replace('-', '')
        chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
        for char in chars:
            if char in strippedPhone:
                raise ValidationError('Phone number cannot contain special characters.')
        if isFieldUnique(strippedPhone, 'user_phone'):
            pass
        else:
            raise ValidationError('Phone number is already in use, please try another.')

    distance = SelectField('Incident Notification Range', choices=[('20','20 miles'),('15','15 miles'),('10','10 miles'),('5','5 miles')], validators=[DataRequired()])

    autocomplete = StringField('Address or Nearby Location', validators=[DataRequired(message='A valid address or location is required.')])

    latitude = HiddenField('Latitude', validators=[DataRequired()])
    def validate_latitude(field, form):
        if field.data == '' or field.data == None:
            raise ValidationError(message='Latitude is empty')

    longitude = HiddenField('Longitude', validators=[DataRequired()])
    def validate_longitude(field, form):
        if field.data == '' or field.data == None:
            raise ValidationError(message='Longitude is empty')

    submit = SubmitField('Register')


###############################################################################
###############################################################################
if __name__ == '__main__':
    pass
