#!/usr/bin/python3
"""
Contains the script to create a superuser in the system.
"""

from werkzeug.security import generate_password_hash
from models.engines.db_storage import DBStorage
from models.user_model import User


def create_superuser():
    """
    A basic script to create a superuser in the system.
    """
    username = input("Enter superuser username: ")
    email = input("Enter superuser email: ")
    password = input("Enter superuser password: ")

    if User.objects(
        username=username
    ).first() or User.objects(email=email).first():
        print("User with that username or email already exists.")
        return

    # Hash the password
    password_hash = generate_password_hash(password)

    # Create the user with the hashed password and role
    admin_user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        role=["admin"],
        is_superuser=True
    )

    admin_user.save()
    print(f"Superuser {username} created successfully.")


if __name__ == '__main__':
    # Establish the database connection
    storage = DBStorage()

    # Create the superuser
    create_superuser()
