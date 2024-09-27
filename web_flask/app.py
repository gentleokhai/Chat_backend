from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from models.engines.db_storage import DBStorage
from views.auth import auth_blueprint  # Import your auth blueprint
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

# Register the authentication routes
app.register_blueprint(auth_blueprint)


if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)
