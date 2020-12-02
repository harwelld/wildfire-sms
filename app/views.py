import json
from app import app
from app.includes.dbaccessor import registerNewCustomer, getCustomers, getIncidentIds, insertIncident
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify


@app.route("/")
def redirectHome():
    return redirect(url_for('home'))


@app.route("/wildfire-sms", methods=['GET', 'POST'])
def home(post=0):
    form = ''
    if request.method == 'POST':
        # TODO: use wtforms and server-side validation
        ##if form.validate_on_submit():
        if form == '':
            customerRecord = request.form.to_dict()
            registerNewCustomer(customerRecord)
            flash('Registration complete', 'success')
            print(customerRecord)
            return redirect(url_for('home', post=1))
        else:
            flash('Error registering please try again', 'error')
    return render_template('index.html', form=form)


@app.route("/getCustomers")
def getCustomers():
    return jsonify(getCustomers())


@app.route("/getIncidents")
def getIncidents():
    return jsonify(getIncidentIds())
