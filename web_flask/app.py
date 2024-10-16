from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from views.auth import auth_blueprint
from views.user_management_00 import user_blueprint
from views.user_management_01 import user_blueprint2
from views.community_management_00 import community_blueprint00
from views.community_management_01 import community_blueprint01
from views.admin_role_management import role_management_bp
from views.therapist_management00 import therapist_blueprint
from views.like_management import like_blueprint
from views.fetch_post import fetch_post_blueprint
from dotenv import load_dotenv
from os import getenv
from views.post import post_blueprint

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set secret key for session management
app.secret_key = getenv('FLASK_SECRET_KEY')

# Configure the JWT manager
app.config['JWT_SECRET_KEY'] = getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

# Initialize Flask-RESTful API
api = Api(app)

# Initialize Flasgger
swagger = Swagger(app)

# Register the authentication routes
app.register_blueprint(auth_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(user_blueprint2)
app.register_blueprint(role_management_bp)
app.register_blueprint(community_blueprint00)
app.register_blueprint(community_blueprint01)
app.register_blueprint(therapist_blueprint)
app.register_blueprint(like_blueprint)
app.register_blueprint(fetch_post_blueprint)


app.register_blueprint(post_blueprint)

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)
