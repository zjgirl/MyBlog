from faker import Faker
from .model import User, Post
from random import randint
from .db import db
from sqlalchemy.exc import IntegrityError

def gen_users(count=100):
    fake = Faker()
    i = 0
    while i < count:
        user = User(
            username = fake.user_name(),
            email = fake.email(),
            password = 'password',
            name = fake.name(),
            location = fake.city(),
            about_me = fake.text(),
            member_since = fake.past_date())
        db.session.add(user)
        try:
            db.session.commit()
            i += 1
        except IntegrityError: # it may create the same username, so need add try...except...
            db.session.rollback()

def gen_posts(count=100):
    fake = Faker()
    i = 0
    users = User.query.all()
    while i < count:
        id = randint(0, len(users)-1)
        post = Post(
            body = fake.text(),
            timestamp = fake.past_date(),
            author_id = users[id].id
        )
        db.session.add(post)
        i += 1
    db.session.commit()

