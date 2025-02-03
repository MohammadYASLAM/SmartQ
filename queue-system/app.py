from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from models import db, User, Admin, Queue
import qrcode
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/queue_db'  # Database credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create tables (Run once to set up your tables)
with app.app_context():
    db.create_all()

# Index page (Admin options)
@app.route('/')
def index():
    return render_template('index.html')

# Route for Admin to log in
@app.route('/admin/login', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        admin_name = request.form['admin_name']
        admin = Admin.query.filter_by(name=admin_name).first()

        if admin:
            session['admin_id'] = admin.id
            flash(f'Welcome back, {admin_name}!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Admin not found. Please register.', 'danger')

    return render_template('login_admin.html')

# Route for Admin to register
@app.route('/admin/register', methods=['GET', 'POST'])
def register_admin():
    if request.method == 'POST':
        admin_name = request.form['admin_name']
        new_admin = Admin(name=admin_name)
        db.session.add(new_admin)
        db.session.commit()
        flash(f'Admin {admin_name} registered successfully!', 'success')
        return redirect(url_for('login_admin'))

    return render_template('register_admin.html')

# Admin Dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('login_admin'))

    admin = Admin.query.get(session['admin_id'])
    queues = Queue.query.filter_by(admin_id=admin.id).all()

    return render_template('admin_dashboard.html', admin=admin, queues=queues)

# Create a new Queue
@app.route('/admin/create_queue', methods=['GET', 'POST'])
def create_queue():
    if 'admin_id' not in session:
        return redirect(url_for('login_admin'))

    if request.method == 'POST':
        queue_name = request.form['queue_name']
        new_queue = Queue(name=queue_name, admin_id=session['admin_id'], number_of_people=0)
        db.session.add(new_queue)
        db.session.commit()

        # Generate QR code for the queue
        qr_link = url_for('join_queue', queue_id=new_queue.id, _external=True)
        img = qrcode.make(qr_link)
        qr_stream = BytesIO()
        img.save(qr_stream)
        qr_stream.seek(0)
        flash(f'Queue {queue_name} created successfully!', 'success')

        return render_template('create_queue.html', qr_code=qr_stream)

    return render_template('create_queue.html')

# Join Queue (User UI)
@app.route('/join_queue/<int:queue_id>', methods=['GET', 'POST'])
def join_queue(queue_id):
    queue = Queue.query.get(queue_id)

    if queue.status == 'paused':
        flash("The queue is currently paused. Please try again later.", 'warning')
        return redirect(url_for('index'))

    if queue.status == 'canceled':
        flash("The queue has been canceled. You cannot join.", 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("You are already in the queue!", 'warning')
            return redirect(url_for('join_queue', queue_id=queue_id))

        # Get the current queue length to assign a position
        queue_length = User.query.filter_by(queue_id=queue_id).count() + 1

        # Create new user
        new_user = User(name=name, email=email, position=queue_length, queue_id=queue_id)
        db.session.add(new_user)
        db.session.commit()

        # Update the queue's number of people
        queue.number_of_people += 1
        db.session.commit()

        flash(f'Joined the queue! Your position is {queue_length}.', 'success')
        return redirect(url_for('view_queue', queue_id=queue.id))

    return render_template('join_queue.html', queue=queue)

# View Queue
@app.route('/queue/<int:queue_id>')
def view_queue(queue_id):
    queue = Queue.query.get(queue_id)
    users = User.query.filter_by(queue_id=queue.id).order_by(User.position).all()

    return render_template('queue.html', queue=queue, users=users)

if __name__ == '__main__':
    app.run(debug=True)
