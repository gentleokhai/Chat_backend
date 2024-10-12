from flask import request
from flask_restful import Resource
from decorators.super_user import superuser_required
from models.user_model import User
from flask import Blueprint

role_management_bp = Blueprint('roles', __name__)


# Class to update user role (only accessible by admin)
class UserRoleUpdateResource(Resource):
    """Handles updating a user's role (restricted to admin)."""

    @superuser_required
    def put(self, user_id):
        """Update a user's role.
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
                role:
                  type: string
                  enum: ["admin", "user"]
                  example: "user"
        responses:
          200:
            description: User role updated successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "User role updated successfully"
          400:
            description: Invalid role provided
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Invalid role provided"
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

        # Update user role
        new_role = data.get('role')
        if new_role not in ["admin", "user"]:
            return {"error": "Invalid role provided"}, 400

        user.role = new_role
        user.save()
        return {"message": f"User role updated successfully"}, 200


role_management_bp.add_url_rule(
    '/api/v1/assign-role/<string:user_id>',
    view_func=UserRoleUpdateResource.as_view('user_view')
)
