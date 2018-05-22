from datetime import datetime, timedelta
import os
import unittest
from app import db, create_app
from app.models import User, Post
from config import basedir, Config
"""
class TestCase(unittest.TestCase):
		#docstring for TestCase"unittest.TestCase) __init__(self, arg):
		#super(TestCase,unittest.TestCase)__init__()
		#self.arg = arg

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
"""
class TestConfig(Config):
	TESTING = True
	SQLALECHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')

class UserModelCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app(TestConfig)
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		#print(self.app.config['SQLALCHEMY_DATABASE_URI'])

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_avatar(self):
		u = User(username='john', email='john@example.com')
		self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
			'd4c74594d841139328695756648b6bd6'
			'?d=identicon&s=128'))

	def test_User(self):
		u = User(username='susan',email='susan@gmail.com')
		db.session.add(u)
		db.session.commit()

		assert u.username == 'susan'
		assert u.email == 'susan@gmail.com'

	def test_follow(self):
		u1 = User(username='john', email='john@example.com')
		u2 = User(username='susan', email='susan@example.com')
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()
		self.assertEqual(u1.followed.all(), [])
		self.assertEqual(u1.followers.all(), [])

		u1.follow(u2)
		os.system("pause")

if __name__ == '__main__':
	unittest.main(verbosity=2)

		
