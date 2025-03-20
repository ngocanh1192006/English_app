from pymongo import MongoClient

# Kết nối MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["flashcards_db"]
collection = db["flashcards_collection"]

def get_flashcards():
    """Lấy danh sách flashcards từ MongoDB"""
    return list(collection.find({}, {"_id": 0}))
