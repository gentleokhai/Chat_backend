from flask import request
from flask_restful import Resource
from flask import Blueprint
from models.community_model import Community
from models.user_model import User
from flask_jwt_extended import get_jwt_identity
from decorators.super_user import superuser_required

community_blueprint01 = Blueprint('community01', __name__)


class UpdateCommunityResource(Resource):
    @superuser_required
    def put(self, community_id):
        """Update a community's details.
        ---
        tags:
          - Community
        parameters:
          - in: path
            name: community_id
            required: true
            type: string
            description: ID of the community
          - in: body
            name: body
            schema:
              type: object
              properties:
                name:
                  type: string
                  example: "Updated Community Name"
                description:
                  type: string
                  example: "Updated description"
        responses:
          200:
            description: Community updated successfully
          404:
            description: Community not found
        """
        data = request.get_json()

        community = Community.objects(id=community_id).first()
        if not community:
            return {"error": "Community not found"}, 404

        current_user = get_jwt_identity()  # Get the currently logged-in user
        user = User.objects(id=current_user).first()  # Fetch the User object

        if not user:
            return {"error": "User not found"}, 404

        community.name = data.get('name', community.name)
        community.description = data.get('description', community.description)
        community.updated_by = user  # Set the updated_by field
        community.save()

        return {
            "message": f"Community {community.name} updated successfully",
            "updated_by": str(user.id)
        }, 200


class DeleteCommunityResource(Resource):
    @superuser_required
    def delete(self, community_id):
        """Delete a community.
        ---
        tags:
          - Community
        parameters:
          - in: path
            name: community_id
            required: true
            type: string
            description: ID of the community
        responses:
          200:
            description: Community deleted successfully
          404:
            description: Community not found
        """
        community = Community.objects(id=community_id).first()
        if not community:
            return {"error": "Community not found"}, 404

        community.delete()
        return {
            "message": f"Community {community.name} deleted successfully"
        }, 200


class ManageModeratorsResource(Resource):
    @superuser_required
    def put(self, community_id):
        """Add or remove moderators for a community.
        ---
        tags:
          - Community
        parameters:
          - in: path
            name: community_id
            required: true
            type: string
            description: ID of the community
          - in: body
            name: body
            schema:
              type: object
              properties:
                add_moderators:
                  type: array
                  items:
                    type: string
                    example: "user_id1"
                remove_moderators:
                  type: array
                  items:
                    type: string
                    example: "user_id2"
        responses:
          200:
            description: Moderators updated successfully
          404:
            description: Community not found
        """
        data = request.get_json()
        add_moderators = data.get('add_moderators', [])
        remove_moderators = data.get('remove_moderators', [])

        community = Community.objects(id=community_id).first()
        if not community:
            return {"error": "Community not found"}, 404

        current_user_id = get_jwt_identity()
        user = User.objects(id=current_user_id).first()

        if not user:
            return {"error": "User not found"}, 404

        # Add moderators
        if add_moderators:
            moderators_to_add = User.objects(id__in=add_moderators)
            community.moderators.extend(moderators_to_add)

        # Remove moderators
        if remove_moderators:
            moderators_to_remove = set(User.objects(id__in=remove_moderators))
            community.moderators = [
                mod for mod in community.moderators
                if mod not in moderators_to_remove
            ]

        community.updated_by = user  # Set the updated_by field
        community.save()
        return {
            "message": f"Moderators updated for {community.name}",
            "updated_by": str(user.id)
        }, 200


community_blueprint01.add_url_rule(
    '/api/v1/community/update-community/<string:community_id>',
    view_func=UpdateCommunityResource.as_view('update_community')
)
community_blueprint01.add_url_rule(
    '/api/v1/community/delete-community/<string:community_id>',
    view_func=DeleteCommunityResource.as_view('delete_community')
)
community_blueprint01.add_url_rule(
    '/api/v1/community/manage-community-moderators/<string:community_id>',
    view_func=ManageModeratorsResource.as_view('manage_community_moderators')
)
