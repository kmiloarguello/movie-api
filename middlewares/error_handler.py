from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
  def __init__(self, app: FastAPI) -> None:
    super().__init__(app)

  async def dispatch(self, request, call_next) -> Response:
    try:
      return await call_next(request)
    except Exception as err:
      return JSONResponse(
        status_code=500,
        content={"message": str(err)}
      )