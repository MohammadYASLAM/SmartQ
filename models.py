from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'  # This specifies the table name in the database

    # Define columns for the User table
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(100), nullable=False)  # Name column, required field
    email = db.Column(db.String(100), nullable=False, unique=True)  # Email column, unique and required
    position = db.Column(db.Integer, nullable=False)  # for user to see current Queue

    # You can add more fields here if needed, for example:
    # joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.name} - Position {self.position}>'

# Add more models as needed, such as Queue, Admin, etc.
