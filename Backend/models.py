from datetime import datetime

from flask_login import UserMixin
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested 

from Backend import db, login_manager, ma
from Backend.constants import available_jobs as available_jobs


@login_manager.user_loader
def user_loader(id):
    return Person.query.get(int(id))


class Person(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    type = db.Column(db.String(20))  # this is the discriminator column

    __mapper_args__ = {
        'polymorphic_on': type,
    }


class User(Person):
    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    email = db.Column(db.String(25), unique=True, nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'user'
    }

    def __repr__(self):
        return f"User('{self.fname} ', '{self.lname}', '{self.email}', '{self.phone}', '{self.location}')"

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class Worker(Person):
    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    email = db.Column(db.String(25), unique=True, nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=False)
    job = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False,
                            default='Insert your personal description here')
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    rate = db.Column(db.Float(2), default=1000.00)
    active = db.Column(db.Boolean, nullable=False, default=True)
    available = db.Column(db.Boolean, nullable=False, default=True)

    __mapper_args__ = {
        'polymorphic_identity': 'worker'
    }

    def __repr__(self):
        return f"Worker('{self.fname} ', '{self.lname}', '{self.email}', '{self.phone}', '{self.job}', '{self.location}')"

class WorkerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Worker

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(15), nullable=False)
    landmark = db.Column(db.String(120), nullable=True)
    user = db.relationship('User', backref='user', lazy=True)

    def __repr__(self):
        return f"Address('{self.user.fname} {self.user.lname} ', '{self.address}', '{self.city}')"

class AddressSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Address

class WorkLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    duration = db.Column(db.String(15), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    accepted = db.Column(db.Boolean, nullable=False, default=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    taskee = db.relationship('User', backref='taskee', lazy=True)
    tasker =  db.relationship('Worker', backref='tasker', lazy=True)
    location = db.relationship('Address', backref='location', lazy=True)

    def __repr__(self):
        return f"Task('{self.taskee}', '{self.tasker} ', '{self.location}', '{self.date}', accepted: '{self.accepted}', completed: '{self.completed}')"
    

class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = WorkLog
    
    taskee = Nested(UserSchema(exclude=['password', 'location', 'type', 'email']))
    tasker = Nested(WorkerSchema(exclude=['password', 'location', 'type', 'email']))
    location = Nested(AddressSchema)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    rater = db.relationship('User', backref='rater', lazy=True)
    worker =  db.relationship('Worker', backref='worker', lazy=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    
class RatingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rating
    
    rater = Nested(UserSchema(exclude=['password', 'location', 'type', 'email', 'phone']))