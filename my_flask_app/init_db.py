from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from app import app, db
from app import User

# Function to initialize the database
def init_db():
    with app.app_context():
        try:
            
            db.create_all()
            print("Database created successfully.")
        except Exception as e:
            print(f"An error occurred while creating the database: {str(e)}")

        # Initial username and password
        username = "admin"
        password = "password"
        
        try:
            # Checks if the user already exists
            if not User.query.filter_by(username=username).first():
                # Creates a new user with a hashed password
                admin_user = User(
                    username=username,
                    password=generate_password_hash(password, method='pbkdf2:sha256')
                )
                # Add the user to the session and commit to the database
                db.session.add(admin_user)
                db.session.commit()
                print(f"User '{username}' created successfully.")
            else:
                print(f"User '{username}' already exists.")
        except Exception as e:
            print(f"An error occurred while creating the user: {str(e)}")

# Run the init_db function when this script is executed
if __name__ == "__main__":
    init_db()
