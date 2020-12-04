import json
from app import app
from app.models import RegistrationForm
from app.includes.dbaccessor import *
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify


@app.route("/")
def redirectHome():
    return redirect(url_for('home'))


@app.route("/wildfire-sms", methods=['GET', 'POST'])
def home():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        # TODO: use wtforms and server-side validation
        ##if form.validate_on_submit():

        customerRecord = request.form.to_dict()
        registerNewCustomer(customerRecord)
        flash('Registration complete', 'success')
        print(customerRecord)
        return redirect(url_for('home'))

    return render_template('index.html', form=form)


@app.route("/getCustomers")
def getCustomers():
    return jsonify(getAllCustomers())


@app.route("/getIncidents")
def getIncidents():
    return jsonify(getAllIncidentIds())


@app.route("/getSmsHistory")
def getSmsHistory():
    return jsonify(getAllSmsHistory())
