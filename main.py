from dotenv import load_dotenv
import os
from fastapi import FastAPI
from pydantic import BaseModel
from database import SessionLocal, User

load_dotenv()

app = FastAPI()

class UserInput(BaseModel):
    name: str
    age: int

@app.post("/user")
def create_user(user: UserInput):
    session = SessionLocal()
    new_user = User(name=user.name, age=user.age)
    session.add(new_user)
    session.commit()
    session.close()
    return {"message": f"{user.name} database mein save hua!"}

@app.get("/users")
def get_users():
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return [{"id": u.id, "name": u.name, "age": u.age} for u in users]

@app.delete('/user/{user_id}')
def delete_user(user_id: int):
    session = SessionLocal()
    user = session.query(User).filter(User.id == user_id).first()
    session.delete(user)
    session.commit()
    session.close()
    return {'message': f'User {user_id} deleted!'}

@app.put('/user/{user_id}')
def update_user(user_id: int,user: UserInput ):
    session = SessionLocal()
    db_user = session.query(User).filter((User.id == user_id)).first()
    db_user.name = user.name
    db_user.age = user.age
    session.commit()
    session.close()
    return {'message': f'User {user_id} updated!'}

import bcrypt
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "yashinsecret123"

fake_db = {}  # temporary storage, real mein database use karenge

@app.post("/signup")
def signup(username: str, password: str):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    fake_db[username] = hashed
    return {"message": "Signup successful!"}

@app.post("/login")
def login(username: str, password: str):
    if username not in fake_db:
        return {"error": "User not found"}
    
    stored_hash = fake_db[username]
    if bcrypt.checkpw(password.encode(), stored_hash):
        token = jwt.encode({"sub": username, "exp": datetime.utcnow() + timedelta(hours=1)}, SECRET_KEY, algorithm="HS256")
        return {"token": token}
    else:
        return {"error": "Wrong password"}
