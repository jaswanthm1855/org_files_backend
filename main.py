from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from exceptions.custom_exception_handler import custom_exception_handler
from exceptions.custom_exceptions import CustomException
from org_files.routes import organisation_file_routes

app = FastAPI()

ALLOWED_ORIGINS = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=organisation_file_routes)


# Add exception handlers to app
app.add_exception_handler(CustomException, custom_exception_handler)
