from jwt import encode

def create_token(data : dict, secret: str):
    return encode(data, secret, algorithm='HS256')