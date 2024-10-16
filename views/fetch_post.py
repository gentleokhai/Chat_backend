# from flask import Blueprint, request, jsonify
# from flask_restful import Resource, Api
# from models.post_model import Post  # Assuming Post is a model in your system

# # Create a Blueprint for post-related endpoints
# fetch_post_blueprint = Blueprint('fetch_post', __name__)
# api = Api(fetch_post_blueprint)

# # Class to fetch all posts in a specific community by community ID
# class PostsByCommunityResource(Resource):
#     def get(self, community_id):
#         page = request.args.get('page', 1, type=int)
#         per_page = request.args.get('per_page', 10, type=int)

#         # Fetch posts by community ID
#         posts = Post.objects(community_id=community_id).paginate(page=page, per_page=per_page)
#         return jsonify({
#             "posts": [{"id": str(post.id), "title": post.title, "content": post.content, "created_at": post.created_at}
#                       for post in posts.items],
#             "total": posts.total,
#             "pages": posts.pages,
#             "current_page": posts.page,
#             "per_page": posts.per_page
#         }), 200

# # Class to fetch a specific post by community ID and post ID
# class PostByCommunityAndPostResource(Resource):
#     def get(self, community_id, post_id):
#         # Fetch the post by community and post ID
#         post = Post.objects(community_id=community_id, id=post_id).first()
#         if post:
#             return jsonify({
#                 "id": str(post.id),
#                 "title": post.title,
#                 "content": post.content,
#                 "created_at": post.created_at,
#                 "community_id": str(post.community_id)
#             }), 200
#         return {"error": "Post not found"}, 404

# # Class to fetch all posts by a specific user
# class PostsByUserResource(Resource):
#     def get(self, user_id):
#         page = request.args.get('page', 1, type=int)
#         per_page = request.args.get('per_page', 10, type=int)

#         # Fetch posts by user ID
#         posts = Post.objects(user_id=user_id).paginate(page=page, per_page=per_page)
#         return jsonify({
#             "posts": [{"id": str(post.id), "title": post.title, "content": post.content, "created_at": post.created_at}
#                       for post in posts.items],
#             "total": posts.total,
#             "pages": posts.pages,
#             "current_page": posts.page,
#             "per_page": posts.per_page
#         }), 200

# # Add URL rules for the resources (endpoints)
# api.add_resource(PostsByCommunityResource, '/api/v1/posts/community/<string:community_id>')
# api.add_resource(PostByCommunityAndPostResource, '/api/v1/posts/community/<string:community_id>/post/<string:post_id>')
# api.add_resource(PostsByUserResource, '/api/v1/posts/user/<string:user_id>')



from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api
from models.post_model import Post  # Assuming Post is a model in your system

# Create a Blueprint for post-related endpoints
fetch_post_blueprint = Blueprint('fetch_post', __name__)
api = Api(fetch_post_blueprint)

# Class to fetch all posts in a specific community by community ID
class PostsByCommunityResource(Resource):
    def get(self, community_id):
        """
        Fetch all posts in a community
        ---
        tags:
          - Posts
        parameters:
          - name: community_id
            in: path
            type: string
            required: true
            description: ID of the community
          - name: page
            in: query
            type: integer
            description: Page number (for pagination)
            default: 1
          - name: per_page
            in: query
            type: integer
            description: Number of posts per page (for pagination)
            default: 10
        responses:
          200:
            description: A list of posts in the community
            schema:
              type: object
              properties:
                posts:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: string
                        example: "60c72b2f9f1b2c5b5d8b5d2e"
                      title:
                        type: string
                        example: "A post title"
                      content:
                        type: string
                        example: "Some content here"
                      created_at:
                        type: string
                        example: "2024-10-15T10:00:00Z"
                total:
                  type: integer
                  example: 25
                pages:
                  type: integer
                  example: 3
                current_page:
                  type: integer
                  example: 1
                per_page:
                  type: integer
                  example: 10
        """
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # Fetch posts by community ID
        posts = Post.objects(community_id=community_id).paginate(page=page, per_page=per_page)
        return jsonify({
            "posts": [{"id": str(post.id), "title": post.title, "content": post.content, "created_at": post.created_at}
                      for post in posts.items],
            "total": posts.total,
            "pages": posts.pages,
            "current_page": posts.page,
            "per_page": posts.per_page
        }), 200


# Class to fetch a specific post by community ID and post ID
class PostByCommunityAndPostResource(Resource):
    def get(self, community_id, post_id):
        """
        Fetch a specific post by community ID and post ID
        ---
        tags:
          - Posts
        parameters:
          - name: community_id
            in: path
            type: string
            required: true
            description: ID of the community
          - name: post_id
            in: path
            type: string
            required: true
            description: ID of the post
        responses:
          200:
            description: A specific post
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "60c72b2f9f1b2c5b5d8b5d2e"
                title:
                  type: string
                  example: "A post title"
                content:
                  type: string
                  example: "Some content here"
                created_at:
                  type: string
                  example: "2024-10-15T10:00:00Z"
                community_id:
                  type: string
                  example: "60c72b2f9f1b2c5b5d8b5d2f"
          404:
            description: Post not found
        """
        # Fetch the post by community and post ID
        post = Post.objects(community_id=community_id, id=post_id).first()
        if post:
            return jsonify({
                "id": str(post.id),
                "title": post.title,
                "content": post.content,
                "created_at": post.created_at,
                "community_id": str(post.community_id)
            }), 200
        return {"error": "Post not found"}, 404


# Class to fetch all posts by a specific user
class PostsByUserResource(Resource):
    def get(self, user_id):
        """
        Fetch all posts by a specific user
        ---
        tags:
          - Posts
        parameters:
          - name: user_id
            in: path
            type: string
            required: true
            description: ID of the user
          - name: page
            in: query
            type: integer
            description: Page number (for pagination)
            default: 1
          - name: per_page
            in: query
            type: integer
            description: Number of posts per page (for pagination)
            default: 10
        responses:
          200:
            description: A list of posts by the user
            schema:
              type: object
              properties:
                posts:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: string
                        example: "60c72b2f9f1b2c5b5d8b5d2e"
                      title:
                        type: string
                        example: "A post title"
                      content:
                        type: string
                        example: "Some content here"
                      created_at:
                        type: string
                        example: "2024-10-15T10:00:00Z"
                total:
                  type: integer
                  example: 10
                pages:
                  type: integer
                  example: 1
                current_page:
                  type: integer
                  example: 1
                per_page:
                  type: integer
                  example: 10
        """
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # Fetch posts by user ID
        posts = Post.objects(user_id=user_id).paginate(page=page, per_page=per_page)
        return jsonify({
            "posts": [{"id": str(post.id), "title": post.title, "content": post.content, "created_at": post.created_at}
                      for post in posts.items],
            "total": posts.total,
            "pages": posts.pages,
            "current_page": posts.page,
            "per_page": posts.per_page
        }), 200


# Add URL rules for the resources (endpoints)
api.add_resource(PostsByCommunityResource, '/api/v1/posts/community/<string:community_id>')
api.add_resource(PostByCommunityAndPostResource, '/api/v1/posts/community/<string:community_id>/post/<string:post_id>')
api.add_resource(PostsByUserResource, '/api/v1/posts/user/<string:user_id>')
