"""
Contains the class DBStorage for MongoDB connections.
"""

from mongoengine import connect
from os import getenv
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


class DBStorage:
    """Interacts with the MongoDB database"""

    def __init__(self):
        """Instantiate a DBStorage object
        and establish a connection to MongoDB"""
        self.db_name = getenv('DB_NAME')
        self.db_host = getenv('DB_HOST', 'localhost')
        self.db_port = int(getenv('DB_PORT', 27017))
        self.db_username = getenv('DB_USERNAME')
        self.db_password = getenv('DB_PASSWORD')

        # Establish MongoDB connection
        self.__connect()

    def __connect(self):
        """Connect to MongoDB"""
        connect(
            db=self.db_name,
            host=self.db_host,
            port=self.db_port,
            username=self.db_username,
            password=self.db_password
        )

    def close(self):
        """Placeholder method for closing the connection if needed"""
        # In MongoEngine, connections are handled automatically.
        pass
