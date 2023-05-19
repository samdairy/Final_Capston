from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime


# adding Flask-Security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

# import the secrets module (from Python) to generate a token for each user
import secrets

# import Flask-Login to check for an authenticated user and store the current user
from flask_login import UserMixin, LoginManager

# import Flask-Marshmallow to help create our Schemas
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=True, default='')
    username = db.Column(db.String(150), nullable=True)
    token = db.Column(db.String, default='', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    meal_plans = db.relationship('MealPlan', backref='owner', lazy=True)

    def __init__(self, email, username, first_name='', last_name='', password=''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.username = username
        self.token = self.set_token(24)

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.password = generate_password_hash(password)
        return self.password

    def __repr__(self):
        return f"User {self.email} has been added to the database!"


class MealPlan(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable=True)
    owner_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, name, description, owner_token):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.owner_token = owner_token

    def set_id(self):
        return str(uuid.uuid4())

    def __repr__(self):
        return f"MealPlan {self.name} has been added to the database!"


class MealPlanSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description']


meal_plan_schema = MealPlanSchema()
meal_plans_schema = MealPlanSchema(many=True)