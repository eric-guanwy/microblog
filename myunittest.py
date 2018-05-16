import os
import unittest

from config import basedir
from app import app, db
from app.models import User, Post

class TestCase(unittest.TestCase):
	"""docstring for TestCase"unittest.TestCase) __init__(self, arg):
		super(TestCase,unittest.TestCase)__init__()
		self.arg = arg
	"""
	def SetUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] =True
		app.config['SQLALECHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
		self.app = app.test_client()
		db.create_all()

	def TearDown(self):
		db.session.remove()
		db.drop_all()

	def test_avatar(self):
		pass

	def test_User(self):
		u = User(username='susan',email='susan@gmail.com')
		db.session.add(u)
		db.session.commit()

		assert u.username == 'susan'
		assert u.email == 'susan@gmail.com'

if __name__ == '__main__':
	unittest.main()

		
