from starlette.requests import Request

from exceptions.custom_exceptions import CustomException


async def custom_exception_handler(request: Request, exc: CustomException):
    """
    It will catch the custom exceptions that are raised and returns a Json response in given format
    status: [SUCCESS, ERROR]
    message: str
    data: {} or None
    """
    from starlette.responses import JSONResponse

    return JSONResponse(
        status_code=exc.status_code,
        content={"status": exc.custom_status, "message": exc.message, "data": exc.data},
    )
