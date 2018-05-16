from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User

class LoginForm(FlaskForm):
	username = StringField(_l('Username'), validators=[DataRequired()])
	password = PasswordField(_l('Password'), validators=[DataRequired()])
	remember_me = BooleanField(_l('Remember_me'))
	submit = SubmitField(_l('Sign In'))

class RegistrationForm(FlaskForm):
	username = StringField(_l('Username'), validators=[DataRequired()])
	email = StringField(_l('Email'), validators=[DataRequired(), Email()])
	password = PasswordField(_l('Password'), validators=[DataRequired()])
	password2 = PasswordField(_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField(_l('Sing Up'))

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError(_('Please use a different username.'))
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError(_('Please use a different email.'))


class EditProfileForm(FlaskForm):
	username = StringField(_l('Username'), validators=[])
	about_me = TextAreaField(_l('About me'), validators=[DataRequired(), Length(min=1,max=140)])
	submit = SubmitField(_l('Submit'))

	def __init__(self, original_username, *args, **kwargs):
		super(EditProfileForm,self).__init__(*args, **kwargs)
		self.original_username = original_username

	def validate_username(self, username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=username.data).first()
			if user is not None:
				raise ValidationError(_('Please use a different username.'))

class PostForm(FlaskForm):
	body = TextAreaField(_l('Say something'), validators=[DataRequired(),Length(min=1,max=140)])
	submit = SubmitField(_l("Submit"))

class ResetPasswordRequestForm(FlaskForm):
	email = StringField(_l('Email'),validators=[DataRequired(), Email()])
	submit = SubmitField(_l('Request Password Reset'))	

class ResetPasswordForm(FlaskForm):
	password = PasswordField(_l('Password'),validators=[DataRequired()])
	password2 = PasswordField(_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField(_l('Request Password Reset'))	