from flask import request
from flask import Blueprint
from flask_restful import Resource
from models.community_model import Community
from models.user_model import User
from flask_jwt_extended import get_jwt_identity, jwt_required
from decorators.super_user import superuser_required

community_blueprint00 = Blueprint('community00', __name__)


class CreateCommunityResource(Resource):
    @superuser_required
    def post(self):
        """Create a new community.
        ---
        tags:
          - Community
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  example: "Python Developers"
                description:
                  type: string
                  example: "A community for Python enthusiasts"
                moderators:
                  type: array
                  items:
                    type: string
                    example: "user_id1"
        responses:
          201:
            description: Community created successfully
          400:
            description: Bad request
        """
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        moderator_ids = data.get('moderators', [])

        # Fetch moderator users from the database
        moderators = User.objects(id__in=moderator_ids)

        if not name:
            return {"error": "Community name is required"}, 400

        # Get the current user (who is creating the community)
        current_user_id = get_jwt_identity()
        current_user = User.objects(id=current_user_id).first()

        if not current_user:
            return {"error": "User not found"}, 404

        # Create a new community
        community = Community(
            name=name,
            description=description,
            moderators=moderators
        )
        community.save(created_by=current_user, updated_by=current_user)

        # Return response with created_by and updated_by
        def get_user_id(user):
            return str(user.id) if user else None

        response = {
            "message": f"Community {community.name} created successfully",
            "created_at": community.created_at.isoformat(),
            "updated_at": community.updated_at.isoformat(),
            "created_by": get_user_id(community.created_by),
            "updated_by": get_user_id(community.updated_by),
            "community_id": str(community.id),
            "moderators": [str(mod.id) for mod in moderators]
        }

        return response, 201


class ReadAllCommunitiesResource(Resource):

    def get(self):
        """Get all communities.
        ---
        tags:
          - Community
        responses:
          200:
            description: A list of communities
        """
        communities = Community.objects()

        # Build the response with created_by,
        # updated_by, created_at, and updated_at
        response = []
        for c in communities:
            response.append({
                "name": c.name,
                "description": c.description,
                "moderators": [str(m.id) for m in c.moderators],
                "created_by": str(c.created_by.id) if c.created_by else None,
                "updated_by": str(c.updated_by.id) if c.updated_by else None,
                "created_at": c.created_at.isoformat(),
                "updated_at": c.updated_at.isoformat()
            })

        return response, 200


class ReadOneCommunityResource(Resource):

    def get(self, community_id):
        """Get details of one community by ID.
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
            description: Community details
          404:
            description: Community not found
        """
        community = Community.objects(id=community_id).first()
        if not community:
            return {"error": "Community not found"}, 404

        def get_user_id(user):
            return str(user.id) if user else None

        response = {
            "name": community.name,
            "description": community.description,
            "moderators": [str(m.id) for m in community.moderators],
            "created_by": get_user_id(community.created_by),
            "updated_by": get_user_id(community.updated_by),
            "created_at": community.created_at.isoformat(),
            "updated_at": community.updated_at.isoformat()
        }

        return response, 200


community_blueprint00.add_url_rule(
    '/api/v1/community/create-community',
    view_func=CreateCommunityResource.as_view('create_community')
)
community_blueprint00.add_url_rule(
    '/api/v1/community/view-all-communities',
    view_func=ReadAllCommunitiesResource.as_view('view_all_communities')
)
community_blueprint00.add_url_rule(
    '/api/v1/community/view-single-communities/<string:community_id>',
    view_func=ReadOneCommunityResource.as_view('view_single_community')
)
