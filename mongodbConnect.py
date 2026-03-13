from pymongo import MongoClient
import env_config

class MongoDBManager:
    _client = None
    _db = None
    _collection = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            if not env_config.MONGODB_URI:
                print("MONGODB_URI not found in environment variables.")
                return None
            try:
                cls._client = MongoClient(env_config.MONGODB_URI)
                # Check connection
                cls._client.admin.command('ping')
            except Exception as e:
                print(f"Failed to initialize or connect MongoClient: {e}")
                cls._client = None
                return None
        return cls._client

    @classmethod
    def get_database(cls, db_name="jobs"):
        client = cls.get_client()
        if client is None:
            return None
        if cls._db is None:
            cls._db = client[db_name]
        return cls._db

    @classmethod
    def get_collection(cls, collection_name="jobsToPost"):
        db = cls.get_database()
        if db is None:
            return None
        if cls._collection is None:
            cls._collection = db[collection_name]
        return cls._collection

# For backward compatibility with existing imports
client = MongoDBManager.get_client()
database = MongoDBManager.get_database()
collection = MongoDBManager.get_collection()
