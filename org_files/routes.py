from typing import Dict

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from starlette.requests import Request

from constants import enums
from org_files import schemas
from org_files.logic_funcs import get_all_organisations, get_organisation_files, upload_file, get_all_organisation_files
from org_files_backend_settings.database import get_db_session

organisation_file_routes = APIRouter(
    prefix="/organisations"
)


@organisation_file_routes.get("", response_model=schemas.GetOrganisationsSuccessSchema)
def get_all_organisations_api(
        db: Session = Depends(get_db_session)
):
    organisation_schemas = get_all_organisations(db=db)
    response = schemas.GetOrganisationsSuccessSchema(
        status=enums.StatusType.SUCCESS.value,
        message="Organisations fetched successfully",
        data=organisation_schemas
    )
    return response


@organisation_file_routes.get("/files", response_model=schemas.GetOrganisationFilesSuccessSchema)
def get_all_organisation_files_api(
        db: Session = Depends(get_db_session)
):
    all_organisation_file_schemas = get_all_organisation_files(db=db)
    response = schemas.GetOrganisationFilesSuccessSchema(
        status=enums.StatusType.SUCCESS.value,
        message="All Organisation Files fetched successfully",
        data=all_organisation_file_schemas
    )
    return response


@organisation_file_routes.get("/{organisation_id}/files", response_model=schemas.GetFilesSuccessSchema)
def get_organisation_files_api(
        organisation_id: str, db: Session = Depends(get_db_session)
):
    organisation_file_schemas = get_organisation_files(organisation_id=organisation_id, db=db)
    response = schemas.GetFilesSuccessSchema(
        status=enums.StatusType.SUCCESS.value,
        message="Organisation Files fetched successfully",
        data=organisation_file_schemas
    )
    return response


@organisation_file_routes.post(
    "/{organisation_id}/files", response_model=schemas.UploadFileSuccessSchema
)
def upload_file_api(
        request: Request,
        organisation_id: str,
        uploaded_file: UploadFile,
        can_replace_file: bool = False,
        db: Session = Depends(get_db_session)
):
    request_schema = schemas.UploadFileRequestSchema(
        uploaded_file=uploaded_file,
        can_replace_file=can_replace_file
    )
    file_schema = upload_file(organisation_id=organisation_id, request_schema=request_schema, db=db)
    response = schemas.UploadFileSuccessSchema(
        status=enums.StatusType.SUCCESS.value,
        message="File Uploaded successfully",
        data=file_schema
    )
    return response
