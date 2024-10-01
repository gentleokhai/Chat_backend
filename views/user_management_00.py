from flask import Blueprint
from flask_restful import Resource
from decorators.super_user import superuser_required
from models.user_model import User


user_blueprint = Blueprint('user', __name__)


class AllUserListResource(Resource):
    """Handles listing all user operations."""

    @superuser_required
    def get(self):
        """Get all users.
        ---
        tags:
          - Users
        responses:
          200:
            description: List of users
            schema:
              type: array
              items:
                type: object
                properties:
                  user_id:
                    type: string
                    example: "abcd1234"
                  username:
                    type: string
                    example: "john_doe"
                  email:
                    type: string
                    example: "john@example.com"
        """
        users = User.objects()
        return [
            {
                'user_id': user.id,
                'username': user.username,
                'email': user.email
            } for user in users
            ], 200


class SingleUserListResource(Resource):
    """get a single user."""

    def get(self, user_id):
        """Get a user by ID.
        ---
        tags:
          - Users
        parameters:
          - in: path
            name: user_id
            required: true
            type: string
            description: The ID of the user to fetch
        responses:
          200:
            description: User found
            schema:
              type: object
              properties:
                user_id:
                  type: string
                  example: "1234abcd"
                username:
                  type: string
                  example: "john_doe"
                email:
                  type: string
                  example: "john@example.com"
          404:
            description: User not found
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "User not found"
        """
        user = User.objects(id=user_id).first()
        if user:
            return {
                'user_id': user.id,
                'username': user.username,
                'email': user.email
                }, 200
        return {'message': 'User not found'}, 404


user_blueprint.add_url_rule(
    '/api/v1/users/view-all',
    view_func=AllUserListResource.as_view('user_list')
)
user_blueprint.add_url_rule(
    '/api/v1/users/<string:user_id>',
    view_func=SingleUserListResource.as_view('user_view')
)
