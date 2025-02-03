from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Admin Model - Represents the administrator of the system
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    queues = db.relationship('Queue', backref='admin', lazy=True)

# User Model - Represents a user who joins the queue
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    position = db.Column(db.Integer, nullable=False)  # Position in the queue
    queue_id = db.Column(db.Integer, db.ForeignKey('queue.id'), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

# Queue Model - Represents a queue managed by an admin
class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    number_of_people = db.Column(db.Integer, default=0)  # Number of people in the queue
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    status = db.Column(db.String(50), default="active")  # active, paused, canceled
    users = db.relationship('User', backref='queue', lazy=True)

    def __repr__(self):
        return f'<Queue {self.name}>'
