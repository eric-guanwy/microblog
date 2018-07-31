from flask import g
from flask_httpauth import HTTPBasicAuth
from app.models import User
from app.api.errors import errors_response

basic_auth = HTTPBasicAuth()

@basic_auth.verify_password
def very_password(username, password):
	user = User.query.filter_by(username=username).first()
	if user is None:
		return False
	g.current_user = user
	return user.checkPassword(password)

@basic_auth.error_handler
def basic_auth_error():
	return errors_response(401)