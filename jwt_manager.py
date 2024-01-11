import os
from dotenv import load_dotenv
from jwt import encode, decode

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")

def create_token(data : dict) -> str:
    return encode(data, key=JWT_SECRET, algorithm='HS256')

def validate_token(token : str) -> dict:
    return decode(token, key=JWT_SECRET, algorithms=['HS256'])