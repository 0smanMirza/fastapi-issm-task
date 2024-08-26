from fastapi import FastAPI, HTTPException, APIRouter
from models.user import User
from config.db import conn
from schemas.user import userEntity


user = APIRouter()


@user.get("/get_all_users", response_model=list[User])
async def get_users():
    users =  conn.notes.notes.find()
    return users



@user.get("/search_user", response_model=User)
async def get_user_by_name(name: str):
    user = conn.notes.notes.find_one({"name": name})
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")



@user.post("/add_user", response_model=User)
async def create_note(user: User):
    user_dict = user.dict(by_alias=True)
    result = conn.notes.notes.insert_one(user_dict)
    if result.inserted_id:
        return userEntity(user_dict)
    raise HTTPException(status_code=400, detail="User could not be created")

