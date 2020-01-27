from flask import render_template, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from application import app
from application.models import user
from application.forms import DareForm, SubmitField
import requests, json
import random

#_____________________________________Main_Service Handling Service3 requests_____________________

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

#_____________________________________ADDING USERS AND VALIDATION_______________________________

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, 
                password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('event'))
    
    return render_template('register.html', title='Register', form=form)

#__________________________________LOGIN____________________________________________________

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
	
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			if next_page:
				return redirect(next_page)
			else:
				return redirect(url_for('home'))
	return render_template('login.html', title='Login', form=form)

#________________________________LOGOUT______________________________________________________


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))
