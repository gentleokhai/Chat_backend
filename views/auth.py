from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import User  # Import your User model


class AuthResource(Resource):
    """Handles user authentication."""

    def post(self):
        """User registration or login.
        ---
        tags:
          - Authentication
        parameters:
          - in: body
            name: body
            description: User registration or login
            required: true
            schema:
              type: object
              properties:
                username:
                  type: string
                  example: "john_doe"
                email:
                  type: string
                  example: "john@example.com"
                password:
                  type: string
                  example: "password123"
        responses:
          201:
            description: User created successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "User created successfully!"
          200:
            description: Access token for the user
            schema:
              type: object
              properties:
                access_token:
                  type: string
                  example: "your_access_token"
          401:
            description: Invalid credentials
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Invalid credentials"
        """
        data = request.get_json()

        # Registration logic
        if 'username' in data and 'password' in data and 'email' in data:
            # Hash the password
            password_hash = generate_password_hash(data['password'])
            user = User(
                username=data['username'],
                email=data['email'],  # Include email here
                password_hash=password_hash  # Use hashed password
            )
            user.save()  # Save the user to the database
            return {'message': 'User created successfully!'}, 201

        # Login logic
        if 'username' in data and 'password' in data:
            user = User.objects(
                username=data['username']
                ).first()
            if user and check_password_hash(
                user.password_hash, data['password']
            ):  # Check hashed password
                access_token = create_access_token(identity=user.id)
                return {'access_token': access_token}, 200

        return {'message': 'Invalid credentials'}, 401
