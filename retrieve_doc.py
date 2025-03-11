import os
import certifi
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

# MongoDB Connection
client = MongoClient(
    MONGODB_URI,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000
)
db = client["resume_db"]
collection = db["resumes"]

def get_all_documents():
    """
    Retrieve all documents from the resumes collection.
    Returns a list of documents sorted by timestamp (newest first).
    """
    documents = list(collection.find({}))
    # Sort documents by timestamp descending (newest first)
    documents.sort(key=lambda doc: doc.get("timestamp", datetime.min), reverse=True)
    return documents

def get_document_by_object_id(object_id):
    """
    Retrieve a document from the collection by its MongoDB _id.
    The object_id should be a string.
    """
    from bson import ObjectId
    try:
        document = collection.find_one({"_id": ObjectId(object_id)})
        return document
    except Exception as e:
        print(f"Error retrieving document: {e}")
        return None
