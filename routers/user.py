from fastapi import APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
from jwt_manager import create_token
from schemas.user import User as UserSchema

user_router = APIRouter()

@user_router.get("/", tags=["root"], include_in_schema=False)
def message() -> dict:
    return HTMLResponse("<h1>Welcome to my movie API</h1>")

@user_router.post("/login", tags=["auth"])
def login(user: UserSchema):
    if user.email == "ca@mi.lo" and user.password == "ca123":
        token = create_token(user.dict())
        return JSONResponse(status_code=200, content={"message": "Login successful", "token": token})
    return JSONResponse(status_code=401, content={"message": "Unauthorized"})

