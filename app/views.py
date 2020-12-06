import json
from app import app
from app.models import RegistrationForm
from app.includes.dbaccessor import *
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from scanFeed import main


@app.route("/")
def redirectHome():
    return redirect(url_for('home'))


@app.route("/wildfire-sms", methods=['GET', 'POST'])
def home():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        customerRecord = request.form.to_dict()
        customerRecord['phone'] = customerRecord['phone'].replace('-', '')
        registerNewCustomer(customerRecord)
        flash('Registration complete', 'success')
        print(customerRecord)
        return redirect(url_for('home'))

    return render_template('index.html', form=form)


@app.route("/getCustomers")
def getCustomers():
    return jsonify(getAllCustomers())


@app.route("/getIncidentIds")
def getIncidentIds():
    return jsonify(getAllIncidentIds())


@app.route("/getSmsHistory")
def getSmsHistory():
    return jsonify(getAllSmsHistory())


# @app.route("/scanFeedMain")
# def scanFeedMain():
#     main()
#     return redirectHome()