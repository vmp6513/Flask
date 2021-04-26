import unittest
import time
from app.models import User
from app import db, create_app


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='enlighten')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='enlighen')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='enlighten')
        self.assertTrue(u.verify_password('enlighten'))
        self.assertFalse(u.verify_password('Enlighten'))

    def test_password_salts_are_random(self):
        u = User(password='enlighten')
        u2 = User(password='enlighten')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_invalid_confirmation_token(self):
        u1 = User(password='cat')
        u2 = User(password='dog')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        u1 = User(password='cat')
        db.session.add(u1)
        db.session.commit()
        token = u1.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u1.confirm(token))
