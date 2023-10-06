from app.models.user import User
from app.db.mongodb import database

user_collection = database.get_collection("users")

async def create_user(user: User):
    user_data = user.dict()
    await user_collection.insert_one(user_data)
