from flask import Blueprint, request
from flask_restful import Resource
from decorators.owner_user import owner_required
from models.user_model import User
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required

user_blueprint2 = Blueprint('user02', __name__)


# Class to update user details (only accessible by the logged-in user)
class UserUpdateResource(Resource):
    """Handles updating a user's details (restricted to the owner)."""

    @owner_required
    def put(self, user_id):
        """Update a user's details.
        ---
        tags:
          - Users
        parameters:
          - in: path
            name: user_id
            required: true
            type: string
            description: The ID of the user to update
          - in: body
            name: body
            required: true
            description: Fields to update
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
                  example: "new_password123"
        responses:
          200:
            description: User updated successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "User john_doe updated successfully"
          404:
            description: User not found
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "User not found"
        """
        data = request.get_json()

        user = User.objects(id=user_id).first()
        if not user:
            return {"error": "User not found"}, 404

        # Update user fields (username, email, etc.)
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)

        # Update password if provided
        new_password = data.get('password')
        if new_password:
            user.password_hash = generate_password_hash(new_password)

        user.save()
        return {"message": f"User {user.username} updated successfully"}, 200


# Class to delete a user (only accessible by the logged-in user)
class UserDeleteResource(Resource):
    """Handles deleting a user (restricted to the owner)."""

    @owner_required
    def delete(self, user_id):
        """Delete a user.
        ---
        tags:
          - Users
        parameters:
          - in: path
            name: user_id
            required: true
            type: string
            description: The ID of the user to delete
        responses:
          200:
            description: User deleted successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "User john_doe deleted successfully"
          404:
            description: User not found
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "User not found"
        """
        user = User.objects(id=user_id).first()
        if not user:
            return {"error": "User not found"}, 404

        user.delete()
        return {"message": f"User {user.username} deleted successfully"}, 200


# Register the Resources
user_blueprint2.add_url_rule(
    '/api/v1/users/update/<string:user_id>',
    view_func=UserUpdateResource.as_view('user_update')
)
user_blueprint2.add_url_rule(
    '/api/v1/users/delete/<string:user_id>',
    view_func=UserDeleteResource.as_view('user_delete')
)
