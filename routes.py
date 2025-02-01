from app import app, db
from flask import request, jsonify
from models import User

@app.route('/join_queue', methods=['POST'])
def join_queue():
    data = request.json  # Get the data sent from the form
    if not data.get('name') or not data.get('email'):
        return jsonify({"message": "Name and Email are required"}), 400

    # Create a new User entry
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User added to queue", "user_id": new_user.id}), 200
