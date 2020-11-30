import json
from app import app
from app.includes.query import registerNewCustomer, getCustomers, insertFireData, getIncidents
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


@app.route("/mapCustomers")
def mapCustomers():
    return jsonify(getCustomers())


@app.route("/testInsertFire")
def testInsertFire():
    fire = {"name":"Cameron Peak Fire","type":"Wildfire","summary":"The Southern Area Gold Type 2 Incident Management Team assumed...","state":"COLORADO","updated":"2020-11-29 20:21:28","lat":"40.609","lng":"-105.879","size":"208,913 Acres","url":"/incident/6964/","id":"6964","contained":"94"}
    insertFireData(fire)
    return jsonify(getIncidents())