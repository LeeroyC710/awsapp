from flask import render_template, redirect, url_for, request
from application import app
from application.forms import DareForm, SubmitField
import requests, json
import random

#------------------       Main_Service Handling Service3             --------------------------

@app.route('/', methods=['GET','POST'])
def generator():
    list=["text-muted", "text-primary", "text-success", "text-info", "text-warning", "text-danger", "text-secondary", "text-dark", "text-light"]
    
    choice=random.choice(list)

    form = DareForm()
    payload={'':''}

    if request.method =='POST':
        
       response = requests.post("http://service3:5003/").json()
       return render_template('home.html', form=form, data=response, choice=choice)
   
    if request.method=='GET':
       return render_template('dare.html', title= 'Dare', form=form)
