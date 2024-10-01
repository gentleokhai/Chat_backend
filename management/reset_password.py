#!/usr/bin/python3
"""
Contains the script to reset a user's password in the system.
"""

from werkzeug.security import generate_password_hash
from models.engines.db_storage import DBStorage
from models.user_model import User


def reset_password():
    """
    Script to reset a user's password.
    """
    email = input(
        "Enter the email of the user whose password you want to reset: "
        )

    user = User.objects(email=email).first()
    if not user:
        print("User with that email does not exist.")
        return

    new_password = input("Enter the new password: ")

    # Hash the new password
    user.password_hash = generate_password_hash(new_password)

    # Save the user with the updated password hash
    user.save()
    print(f"Password for {user.username} has been successfully updated.")


if __name__ == '__main__':
    # Establish the database connection
    storage = DBStorage()

    # Reset the password
    reset_password()
