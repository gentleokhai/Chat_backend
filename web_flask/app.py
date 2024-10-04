from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from models.engines.db_storage import DBStorage
from views.auth import auth_blueprint
from views.user_management_00 import user_blueprint
from views.user_management_01 import user_blueprint2
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

# Create a DBStorage instance to manage MongoDB connections
storage = DBStorage()

# Initialize Flask-RESTful API
api = Api(app)

# Initialize Flasgger
swagger = Swagger(app)

# Register the authentication routes
app.register_blueprint(auth_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(user_blueprint2)


app.register_blueprint(post_blueprint)

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)
