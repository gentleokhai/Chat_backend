from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from models.engines.db_storage import DBStorage
from views.auth import AuthResource  # Import your AuthResource
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure the JWT manager
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

# Create a DBStorage instance to manage MongoDB connections
storage = DBStorage()

# Initialize Flask-RESTful API
api = Api(app)

# Initialize Flasgger
swagger = Swagger(app)

# Register the authentication route
api.add_resource(AuthResource, '/api/v1/auth')


@app.route('/')
def index():
    """A simple route that confirms MongoDB connection.
    ---
    responses:
      200:
        description: MongoDB connected
    """
    return "MongoDB connected using Flask and DBStorage!"


if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)
