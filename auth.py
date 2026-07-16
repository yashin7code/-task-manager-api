import bcrypt

password = "mypassword123"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(hashed)

# check karna
check = bcrypt.checkpw(password.encode('utf-8'), hashed)
print(check)  # True

from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "yashinsecret123"

def create_token(username):
    data = {"sub": username, "exp": datetime.utcnow() + timedelta(hours=1)}
    token = jwt.encode(data, SECRET_KEY, algorithm="HS256")
    return token

token = create_token("Yashin")
print(token)

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except:
        return None

result = verify_token(token)
print(result)