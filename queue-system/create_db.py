from app import db, app
with app.app_context():
    db.drop_all()  # This will delete all tables (be careful!)
    db.create_all()
print("Database tables recreated successfully!")

