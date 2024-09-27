# views/auth.py

from flask import Blueprint, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import User  # Import your User model

auth_blueprint = Blueprint('auth', __name__)


class RegistrationResource(Resource):
    """Handles user registration."""

    def post(self):
        """User registration.
        ---
        tags:
          - Authentication
        parameters:
          - in: body
            name: body
            description: User registration
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

        return {'message': 'Missing required fields.'}, 400


class LoginResource(Resource):
    """Handles user login."""

    def post(self):
        """User login.
        ---
        tags:
          - Authentication
        parameters:
          - in: body
            name: body
            description: User login
            required: true
            schema:
              type: object
              properties:
                username:
                  type: string
                  example: "john_doe"
                password:
                  type: string
                  example: "password123"
        responses:
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

        # Login logic
        if 'username' in data and 'password' in data:
            user = User.objects(
                username=data['username']
            ).first()
            if user and check_password_hash(
                user.password_hash, data['password']
            ):
                access_token = create_access_token(identity=user.id)
                return {'access_token': access_token}, 200

        return {'message': 'Invalid credentials'}, 401


# Register the resources to the Blueprint
auth_blueprint.add_url_rule(
    '/api/v1/auth/register', view_func=RegistrationResource.as_view('register')
)
auth_blueprint.add_url_rule(
    '/api/v1/auth/login', view_func=LoginResource.as_view('login')
    )
