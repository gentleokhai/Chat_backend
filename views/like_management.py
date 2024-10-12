from flask import Blueprint, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from decorators.owner_user import owner_required
from models.like_model import Like
from decorators.super_user import superuser_required

like_blueprint = Blueprint('like', __name__)


# Class to add a like
class LikeCreateResource(Resource):
    """Handles creating a new like."""

    def post(self):
        """Create a new like.
        ---
        tags:
          - Likes
        parameters:
          - in: body
            name: body
            required: true
            description: Fields to create a like
            schema:
              type: object
              properties:
                post_id:
                  type: string
                  example: "123456"
                comment_id:
                  type: string
                  example: "654321"
                therapist_id:
                  type: string
                  example: "abcdef"
                value:
                  type: integer
                  enum: [1, -1]
                  example: 1
        responses:
          201:
            description: Like created successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Like created successfully"
          400:
            description: Invalid input
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Invalid input"
        """
        data = request.get_json()
        user_id = request.user.id  # Get the logged-in user ID

        # Check if at least one ID is provided
        if not (
            data.get('post_id') or
            data.get('comment_id') or
            data.get('therapist_id')
        ):
            return {
                "error": "post_id, comment_id, or therapist_id is required"
            }, 400

        # Check if the user has already liked the post/comment/therapist
        existing_like = Like.objects(
            user_id=user_id,
            post_id=data.get('post_id'),
            comment_id=data.get('comment_id'),
            therapist_id=data.get('therapist_id')
        ).first()

        if existing_like:
            return {
                "error": "like a post, comment, or therapist only once."
            }, 400

        like = Like(
            user_id=user_id,
            post_id=data.get('post_id'),
            comment_id=data.get('comment_id'),
            therapist_id=data.get('therapist_id'),
            value=data.get('value')
        )
        like.save()
        return {"message": "Like created successfully"}, 201


# Class to fetch all likes (superuser required)
class LikeListResource(Resource):
    """Handles fetching all likes (restricted to superusers)."""

    @superuser_required
    def get(self):
        """Fetch all likes.
        ---
        tags:
          - Likes
        responses:
          200:
            description: List of all likes
            schema:
              type: array
              items:
                type: object
                properties:
                  user_id:
                    type: string
                    example: "123456"
                  post_id:
                    type: string
                    example: "654321"
                  comment_id:
                    type: string
                    example: "abcdef"
                  therapist_id:
                    type: string
                    example: "ghijkl"
                  value:
                    type: integer
                    example: 1
        """
        likes = Like.objects()
        return [{"user_id": str(like.user_id),
                 "post_id": str(like.post_id),
                 "comment_id": str(like.comment_id),
                 "therapist_id": str(like.therapist_id),
                 "value": like.value} for like in likes
                ], 200


# Class to fetch likes by user ID
class LikeByUserResource(Resource):
    """Handles fetching likes for a specific user."""

    @owner_required
    def get(self, user_id):
        """Fetch all likes by a specific user.
        ---
        tags:
          - Likes
        parameters:
          - in: path
            name: user_id
            required: true
            type: string
            description: The ID of the user
        responses:
          200:
            description: List of likes by the user
            schema:
              type: array
              items:
                type: object
                properties:
                  post_id:
                    type: string
                    example: "654321"
                  comment_id:
                    type: string
                    example: "abcdef"
                  therapist_id:
                    type: string
                    example: "ghijkl"
                  value:
                    type: integer
                    example: 1
        """
        likes = Like.objects(user_id=user_id)
        return [{"post_id": str(like.post_id),
                 "comment_id": str(like.comment_id),
                 "therapist_id": str(like.therapist_id),
                 "value": like.value} for like in likes
                ], 200


# Class to fetch likes for a specific post
class LikeByPostResource(Resource):
    """Handles fetching likes for a specific post."""

    def get(self, post_id):
        """Fetch all likes for a specific post.
        ---
        tags:
          - Likes
        parameters:
          - in: path
            name: post_id
            required: true
            type: string
            description: The ID of the post
        responses:
          200:
            description: List of likes for the post
            schema:
              type: array
              items:
                type: object
                properties:
                  user_id:
                    type: string
                    example: "123456"
                  value:
                    type: integer
                    example: 1
        """
        likes = Like.objects(post_id=post_id)
        return [{"user_id": str(like.user_id),
                 "value": like.value} for like in likes
                ], 200


# Class to fetch likes for a specific comment
class LikeByCommentResource(Resource):
    """Handles fetching likes for a specific comment."""

    def get(self, comment_id):
        """Fetch all likes for a specific comment.
        ---
        tags:
          - Likes
        parameters:
          - in: path
            name: comment_id
            required: true
            type: string
            description: The ID of the comment
        responses:
          200:
            description: List of likes for the comment
            schema:
              type: array
              items:
                type: object
                properties:
                  user_id:
                    type: string
                    example: "123456"
                  value:
                    type: integer
                    example: 1
        """
        likes = Like.objects(comment_id=comment_id)
        return [{"user_id": str(like.user_id),
                 "value": like.value} for like in likes
                ], 200


# Class to fetch likes for a specific therapist
class LikeByTherapistResource(Resource):
    """Handles fetching likes for a specific therapist."""

    def get(self, therapist_id):
        """Fetch all likes for a specific therapist.
        ---
        tags:
          - Likes
        parameters:
          - in: path
            name: therapist_id
            required: true
            type: string
            description: The ID of the therapist
        responses:
          200:
            description: List of likes for the therapist
            schema:
              type: array
              items:
                type: object
                properties:
                  user_id:
                    type: string
                    example: "123456"
                  value:
                    type: integer
                    example: 1
        """
        likes = Like.objects(therapist_id=therapist_id)
        return [{"user_id": str(like.user_id),
                 "value": like.value} for like in likes
                ], 200


# Class to update a like by ID
class LikeUpdateResource(Resource):
    """Handles updating an existing like."""

    @owner_required
    def put(self, like_id):
        """Update an existing like.
        ---
        tags:
          - Likes
        parameters:
          - in: path
            name: like_id
            required: true
            type: string
            description: The ID of the like to update
          - in: body
            name: body
            required: true
            description: Fields to update
            schema:
              type: object
              properties:
                value:
                  type: integer
                  enum: [1, -1]
                  example: 1
        responses:
          200:
            description: Like updated successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Like updated successfully"
          404:
            description: Like not found
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Like not found"
        """
        data = request.get_json()
        like = Like.objects(id=like_id).first()
        if not like:
            return {"error": "Like not found"}, 404

        # Update the value
        like.value = data.get('value', like.value)
        like.save()
        return {"message": "Like updated successfully"}, 200


# Class to delete a like
class LikeDeleteResource(Resource):
    """Handles deleting a like."""

    @owner_required
    def delete(self, like_id):
        """Delete a like.
        ---
        tags:
          - Likes
        parameters:
          - in: path
            name: like_id
            required: true
            type: string
            description: The ID of the like to delete
        responses:
          200:
            description: Like deleted successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Like deleted successfully"
          404:
            description: Like not found
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Like not found"
        """
        like = Like.objects(id=like_id).first()
        if not like:
            return {"error": "Like not found"}, 404

        like.delete()
        return {"message": "Like deleted successfully"}, 200


like_blueprint.add_url_rule(
    '/api/v1/like/create-like',
    view_func=LikeCreateResource.as_view('like_create')
)
like_blueprint.add_url_rule(
    '/api/v1/all-likes',
    view_func=LikeListResource.as_view('like_list')
)
like_blueprint.add_url_rule(
    '/api/v1/like/user-like/<string:user_id>',
    view_func=LikeByUserResource.as_view('like_by_user')
)
like_blueprint.add_url_rule(
    '/api/v1/like/post-like/<string:post_id>',
    view_func=LikeByPostResource.as_view('like_by_post')
)
like_blueprint.add_url_rule(
    '/api/v1/like/comment-like/<string:comment_id>',
    view_func=LikeByCommentResource.as_view('like_by_comment')
)
like_blueprint.add_url_rule(
    '/api/v1/like/therapist-like/<string:therapist_id>',
    view_func=LikeByTherapistResource.as_view('like_by_therapist')
)
like_blueprint.add_url_rule(
    '/api/v1/like/update-like/<string:like_id>',
    view_func=LikeUpdateResource.as_view('like_update')
)
like_blueprint.add_url_rule(
    '/api/v1/like/delete-like/<string:like_id>',
    view_func=LikeDeleteResource.as_view('like_delete')
)
