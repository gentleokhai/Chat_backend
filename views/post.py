from flask import Blueprint, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.post_model import Post
from models.user_model import User
from models.community_model import Community
from decorators.owner_user import owner_required

post_blueprint = Blueprint('post', __name__)


class PostResource(Resource):
    """Handles creating, editing, and deleting posts."""

    @jwt_required()
    def post(self):
        """Create a new post.
        ---
        tags:
          - Posts
        parameters:
          - in: body
            name: body
            description: Create a new post
            required: true
            schema:
              type: object
              properties:
                title:
                  type: string
                  example: "My First Post"
                body:
                  type: string
                  example: "This is the body of my first post."
                community_id:
                  type: string
                  example: "605c72efc83f7f57e063dbb1"
        responses:
          201:
            description: Post created successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Post created successfully!"
        """
        data = request.get_json()
        user_id = get_jwt_identity()

        # Create a new post
        if 'title' in data and 'body' in data and 'community_id' in data:
            post = Post(
                title=data['title'],
                body=data['body'],
                user_id=user_id,
                community_id=data['community_id']
            )
            post.save()  # Save the post to the database
            return {'message': 'Post created successfully!'}, 201

        return {'message': 'Missing required fields.'}, 400

    @jwt_required()
    @owner_required
    def put(self, post_id):
        """Edit an existing post.
        ---
        tags:
          - Posts
        parameters:
          - in: path
            name: post_id
            required: true
            type: string
          - in: body
            name: body
            description: Edit a post
            required: true
            schema:
              type: object
              properties:
                title:
                  type: string
                  example: "Updated Post Title"
                body:
                  type: string
                  example: "Updated content of the post."
        responses:
          200:
            description: Post updated successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Post updated successfully!"
          404:
            description: Post not found
        """
        data = request.get_json()
        user_id = get_jwt_identity()

        post = Post.objects(id=post_id, user_id=user_id).first()

        if post:
            if 'title' in data:
                post.title = data['title']
            if 'body' in data:
                post.body = data['body']
            post.save()
            return {'message': 'Post updated successfully!'}, 200

        return {'message': 'Post not found.'}, 404

    @owner_required
    def delete(self, post_id):
        """Delete a post.
        ---
        tags:
          - Posts
        parameters:
          - in: path
            name: post_id
            required: true
            type: string
        responses:
          200:
            description: Post deleted successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Post deleted successfully!"
          404:
            description: Post not found
        """
        user_id = get_jwt_identity()

        post = Post.objects(id=post_id, user_id=user_id).first()

        if post:
            post.delete()
            return {'message': 'Post deleted successfully!'}, 200

        return {'message': 'Post not found.'}, 404


# Register the resources to the Blueprint
post_blueprint.add_url_rule(
    '/api/v1/posts',
    view_func=PostResource.as_view('create_post'),
    methods=['POST']
)
post_blueprint.add_url_rule(
    '/api/v1/posts/<string:post_id>',
    view_func=PostResource.as_view('edit_delete_post'),
    methods=['PUT', 'DELETE']
)
