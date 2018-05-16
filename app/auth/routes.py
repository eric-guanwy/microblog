from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user
from flask_babel import _, get_locale
from app import app,db
from .forms import LoginForm, RegistrationForm
from app.models import User, Post
from datetime import datetime
from . import bp

@bp.route('/register', methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()

	if form.validate_on_submit():		
		user = User(username=form.username.data, email=form.email.data)
		user.setPassword(password=form.password.data)
		db.session.add(user)
		db.session.commit()
		flash(_('Congratulations, you\'re now a registered user!'))
		app.logger.info('user {} registered.'.format(form.username.data))
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html',title='Register', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))	
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.checkPassword(form.password.data):
			flash(_('Invalid username or password!'))
			return redirect(url_for('auth.login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('auth/login.html',title='Sign In',form=form)