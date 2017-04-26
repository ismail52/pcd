#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import time
from flask import Flask, render_template, request,redirect
from simpleuser import comments_link_and_date
import facebook
app = Flask(__name__, template_folder='../html-templates', static_folder='../assets')

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/simpleUser')
def simpleUser():
    return render_template('simpleUser.html')
@app.route('/company')
def company():
    return render_template('company.html')
@app.route('/manual')
def manual():
    return render_template('manual.html')

@app.route('/chart_simpleuser')
def chart_simpleuser():
    return render_template('chart_simpleuser.html')

@app.route('/chart_company')
def chart_company():
    return render_template('chart_company.html')

@app.route('/chart_manualsearch')
def chart_manualsearch():
    return render_template('chart_manualsearch.html')

@app.route('/test', methods=['POST'])
def test():
	
	return str(comments_link_and_date("cnninternational", request.form['keyword'])[0])	    	
app.run('0.0.0.0', 600)