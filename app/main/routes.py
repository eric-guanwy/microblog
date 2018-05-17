from flask import render_template, flash, redirect, url_for, request, g,\
jsonify,current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import  EditProfileForm, PostForm
from app.models import User, Post
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_babel import _, get_locale
from app.translate import translate
from langdetect import detect
from app.main import bp


@bp.before_request
def before_request():
	if current_user.is_authenticated: 
		current_user.last_seen = datetime.utcnow()
		db.session.commit()
		#print('get_locale():',str(get_locale()))
	g.locale = str(get_locale())
	
	if g.locale == 'zh_Hans_CN':
		g.locale = 'zh_CN'
	#print('g.locale:',g.locale) 
	

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	form = PostForm()
	if request.method=='POST':
		if form.validate_on_submit():
			#language = guess_language(form.body.data)
			try:
				language = detect(form.body.data)
			except Exception as e:
				language = ''
				app.logger.error(e)

			post = Post(body=form.body.data,author=current_user,
						timestamp=datetime.utcnow(),language=language)			
			db.session.add(post)
			db.session.commit()
			flash(_('Your post is now live!'))
			return redirect(url_for('main.index')) 
	page = request.args.get('page',1,type=int)
	posts = current_user.followed_posts().paginate(page, current_app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
	prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
	return render_template('index.html',title=_('Home'), user=current_user, form= form, 
		posts=posts.items,prev_url=prev_url, next_url=next_url)


@bp.route('/explore')
@login_required
def explore():
	page = request.args.get('page',1,type=int)
	posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'],False)
	prev_url = url_for('main.explore', page=posts.prev_num) if posts.prev_num else None
	next_url = url_for('main.explore', page=posts.next_num) if posts.next_num else None
	return render_template('index.html', title='Explore', posts=posts.items, prev_url=prev_url, next_url=next_url)


@bp.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first()
	page = request.args.get('page',1, type=int)
	if user is None:
		flash(_('user %(username)s not found.', username=username))
		return redirect(url_for('main.index'))
	posts = user.posts.order_by(Post.timestamp.desc()).paginate(page,current_app.config['POSTS_PER_PAGE'],False)
	prev_url = url_for('main.user', username=username, page=posts.prev_num) if posts.has_prev else None
	next_url = url_for('main.user', username=username, page=posts.next_num) if posts.has_next else None	
	return render_template('user.html', user=user, posts=posts.items, prev_url=prev_url, next_url=next_url)

@bp.route('/editprofile',methods=['GET','POST'])
@login_required
def edit_profile():
	form = EditProfileForm(original_username=current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash(_('your changes has been saved.'))
		return redirect(url_for('main.edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='Edit Profile', form = form)

@bp.route('/follow/<username>')
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
	return redirect(url_for('main.user',username=username))

@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash(_('User %(username)s Not Found.', username=username))
		return redirect(url_for('main.index'))
	if user == current_user:
		flash(_('You cannot unfollow yourself.'))
		return redirect(url_for('main.user',username=username))

	current_user.unfollow(user)
	db.session.commit()
	flash(_('You have stop follow %(username)s now.', username=username))
	return redirect(url_for('main.user',username=username))

@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():	
	return jsonify({'text': "{}".format(translate(request.form['text'],
										request.form['source_language'],
										request.form['dest_language']))})


@bp.route('/upload', methods=['GET','POST'])
@login_required
def upload():
	if request.method == 'POST':
		f = request.files['file']
		basepath = os.path.dirname(__file__)
		upload_path = os.path.join(basepath, 'static\\uploads', secure_filename(f.filename))
		f.save(upload_path)
		return redirect(url_for('main.upload'))
	return render_template('upload.html')