"""
MongoDB Database Connection and Operations
"""
from pymongo import MongoClient
from datetime import datetime
import os

# MongoDB Connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client['criminal_db']
criminals_collection = db['criminals']

# Create indexes
criminals_collection.create_index('name', unique=True)

def insert_criminal(criminal_data):
    """Insert criminal record into database"""
    try:
        criminal_data['created_at'] = datetime.now()
        result = criminals_collection.insert_one(criminal_data)
        return result.inserted_id
    except Exception as e:
        print(f"Error inserting criminal: {e}")
        return None

def get_criminal_by_name(name):
    """Get criminal record by name"""
    return criminals_collection.find_one({'name': name})

def get_all_criminals():
    """Get all criminal records"""
    return list(criminals_collection.find())

def get_all_encodings():
    """Get all face encodings with names"""
    criminals = criminals_collection.find({'face_encoding': {'$exists': True}})
    encodings = []
    names = []
    records = []
    
    for criminal in criminals:
        if criminal.get('face_encoding'):
            encodings.append(criminal['face_encoding'])
            names.append(criminal['name'])
            records.append(criminal)
    
    return encodings, names, records

def update_criminal(name, update_data):
    """Update criminal record"""
    return criminals_collection.update_one(
        {'name': name},
        {'$set': update_data}
    )

def criminal_exists(name):
    """Check if criminal exists"""
    return criminals_collection.find_one({'name': name}) is not None

def delete_criminal(name):
    """Delete criminal from database"""
    return criminals_collection.delete_one({'name': name})
