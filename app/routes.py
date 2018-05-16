from flask import render_template, flash, redirect, url_for, request, g
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import app,db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email
from app.models import User, Post
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_babel import _, get_locale
import os

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():	
	user = current_user
	form = PostForm()
	page = request.args.get('page',1,type=int)
	if request.method=='POST':
		if form.validate_on_submit():
			post = Post(body=form.body.data,timestamp=datetime.utcnow(),author=user)			
			db.session.add(post)
			db.session.commit()
			flash(_('Your post is now live!'))
			return redirect(url_for('index')) 
	posts = user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('index', page=posts.next_num) if posts.has_next else None
	prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
	return render_template('index.html',title=_('Home'), user=user, form= form, 
		posts=posts.items,prev_url=prev_url, next_url=next_url)


@app.route('/explore')
@login_required
def explore():
	page = request.args.get('page',1,type=int)
	posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'],False)
	prev_url = url_for('index', page=posts.prev_num) if posts.prev_num else None
	next_url = url_for('index', page=posts.next_num) if posts.next_num else None
	return render_template('index.html', title='Explore', posts=posts.items, prev_url=prev_url, next_url=next_url)

@app.before_request
def before_request():
	if current_user.is_authenticated: 
		current_user.last_seen = datetime.utcnow()
		db.session.commit()
	g.locale = str(get_locale())
	if g.locale == 'zh_Hans_CN':
		g.locale = 'zh_CN'
	#print('g.locale:',g.locale) 


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first()
	page = request.args.get('page',1, type=int)
	if user is None:
		flash(_('user %(username)s not found.', username=username))
		return redirect(url_for('index'))
	posts = user.posts.order_by(Post.timestamp.desc()).paginate(page,app.config['POSTS_PER_PAGE'],False)
	prev_url = url_for('user', username=username, page=posts.prev_num) if posts.has_prev else None
	next_url = url_for('user', username=username, page=posts.next_num) if posts.has_next else None	
	return render_template('user.html', user=user, posts=posts.items, prev_url=prev_url, next_url=next_url)

@app.route('/editprofile',methods=['GET','POST'])
@login_required
def edit_profile():
	form = EditProfileForm(original_username=current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash(_('your changes has been saved.'))
		return redirect(url_for('edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='Edit Profile', form = form)

@app.route('/follow/<username>')
@login_required
def follow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash(_('User %(username)s Not Found.', username =username))
		return redirect('index')
	if user == current_user:
		flash(_('You cannot follow yourself.'))
		return redirect('user',username=username)

	current_user.follow(user)
	db.session.commit()
	flash(_('You are following %(username)s.',username =username))
	return redirect(url_for('user',username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash(_('User %(username)s Not Found.', username=username))
		return redirect(url_for('index'))
	if user == current_user:
		flash(_('You cannot unfollow yourself.'))
		return redirect(url_for('user',username=username))

	current_user.unfollow(user)
	db.session.commit()
	flash(_('You have stop follow %(username)s now.', username=username))
	return redirect(url_for('user',username=username))

@app.route('/reset_password_request', methods=['GET','POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			send_password_reset_email(user)
		flash(_('Check your email for instructions to reset your password.'))
		return redirect(url_for('index'))
	return render_template('reset_password_request.html', title=_('Reset Password'), form=form)

@app.route('/reset_password/<token>', methods=['GET','POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.setPassword(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash(_('Your password has been reset.'))
		return redirect(url_for('auth.login'))
	return render_template('reset_password.html',form=form)


@app.route('/upload', methods=['GET','POST'])
@login_required
def upload():
	if request.method == 'POST':
		f = request.files['file']
		basepath = os.path.dirname(__file__)
		upload_path = os.path.join(basepath, 'static\\uploads', secure_filename(f.filename))
		f.save(upload_path)
		return redirect(url_for('upload'))
	return render_template('upload.html')
