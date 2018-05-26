from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from app.models import User

class LoginForm(FlaskForm):
	username = StringField(_l('Username'), 
		render_kw={"placeholder":_l("Username"),"type":"text","autocomplete":"username"},
		validators=[DataRequired()])
	password = PasswordField(_l('Password'),
		render_kw={"placeholder": _l("Password"), "type":"password","autocomplete":"current-password"},
		validators=[DataRequired()])
	remember_me = BooleanField(_l('Remember_me'))
	submit = SubmitField(_l('Sign In'))

class RegistrationForm(FlaskForm):
	username = StringField(_l('Username'),
		render_kw={"placeholder":_l("Username"),"type":"text"},
		validators=[DataRequired()])
	email = StringField(_l('Email'),
		render_kw={"placeholder": _l("Email : yourname@example.com"), "type":"text","autocomplete":"email"}, 
		validators=[DataRequired(), Email()])
	password = PasswordField(_l('Password'), 
		render_kw={"placeholder": _l("Password"), "type":"password","autocomplete":"new-password"},
		validators=[DataRequired()])
	password2 = PasswordField(_l('Repeat Password'),
		render_kw={"placeholder": _l("Repeat Password"), "type":"password","autocomplete":"new-password"},
		validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField(_l('Sing Up'))

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError(_('Please use a different username.'))
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError(_('Please use a different email.'))

class ResetPasswordRequestForm(FlaskForm):
	email = StringField(_l('Email'),
		render_kw={"placeholder": _l("Email: yourname@example.com"), "type":"text","autocomplete":"email"}, 
		validators=[DataRequired(), Email()])
	submit = SubmitField(_l('Request Password Reset'))	

class ResetPasswordForm(FlaskForm):
	password = PasswordField(_l('Password'),
		render_kw={"placeholder": _l("Password"), "type":"password","autocomplete":"new-password"},
		validators=[DataRequired()])
	password2 = PasswordField(_l('Repeat Password'), 
		render_kw={"placeholder": _l("Repeat Password"), "type":"password","autocomplete":"new-password"},
		validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField(_l('Request Password Reset'))	