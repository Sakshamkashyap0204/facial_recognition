from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['criminal_db']

# Delete all criminals
result = db.criminals.delete_many({})
print(f"Deleted {result.deleted_count} criminals from database")
print("Database cleared successfully")
