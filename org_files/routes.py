from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

import models
from constants import enums
from org_files import schemas
from org_files.logic_funcs import get_all_organisations, get_organisation_files, upload_file
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
    "/{organisation_id}/files", response_model=schemas.GetFilesSuccessSchema
)
def upload_file_api(
        request_schema: schemas.UploadFileRequestSchema, db: Session = Depends(get_db_session)
):
    file_schema = upload_file(request_schema=request_schema, db=db)
    response = schemas.UploadFileSuccessSchema(
        status=enums.StatusType.SUCCESS.value,
        message="File Uploaded successfully",
        data=file_schema
    )
    return response
