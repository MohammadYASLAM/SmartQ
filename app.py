from flask import Flask, render_template, request, jsonify
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/queue_db'  # Update with your database credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/join_queue', methods=['POST'])
def join_queue():
    name = request.json.get('name')
    email = request.json.get('email')

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "You are already in the queue!"}), 400

    # Get the current queue length to assign a position
    queue_length = User.query.count() + 1  # Position is the next number in the queue

    # Create the new user with the correct position
    new_user = User(name=name, email=email, position=queue_length)
    
    # Add to database
    db.session.add(new_user)
    db.session.commit()

    # Return the position of the user
    return jsonify({
        "message": f"Joined the queue successfully! Your position is {queue_length}.",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "position": new_user.position
        }
    })

@app.route('/queue')
def view_queue():
    users = User.query.order_by(User.position).all()  # Show users by their queue position
    return render_template('queue.html', users=users)

@app.route('/leave_queue/<int:user_id>', methods=['POST'])
def leave_queue(user_id):
    user_to_leave = User.query.get(user_id)

    if user_to_leave:
        db.session.delete(user_to_leave)
        db.session.commit()

        return jsonify({"message": f"Successfully left the queue!"})
    
    return jsonify({"message": "User not found in the queue!"}), 404


if __name__ == '__main__':
    app.run(debug=True)
