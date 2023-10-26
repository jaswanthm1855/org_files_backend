import os.path
import shutil
from typing import List

from fastapi import UploadFile
from sqlalchemy.orm import Session

import models
from constants.plain_constants import UPLOAD_DIR_BASE_PATH
from exceptions.custom_exceptions import CustomException
from exceptions.exception_messages import ORGANISATION_DOES_NOT_EXISTS_EXCEPTION, FILE_ALREADY_EXISTS, \
    UNABLE_TO_PROCESS_FILE
from org_files import schemas
from utils.get_random_id_string import get_random_uuid_string_for_primary_key


def get_all_organisations(db: Session) -> List[schemas.OrganisationSchema]:
    organisation_objs = db.query(models.Organisation).all()
    organisation_schemas = [
        schemas.OrganisationSchema(**org_obj.__dict__) for org_obj in organisation_objs
    ]
    return organisation_schemas


def get_organisation_files(organisation_id: str, db: Session) -> List[schemas.FileSchema]:
    file_objs = db.query(models.OrganisationFile).filter(models.OrganisationFile.id == organisation_id).all()
    file_schemas = [
        schemas.FileSchema(**file_obj.__dict__) for file_obj in file_objs
    ]
    return file_schemas


def upload_file(request_schema: schemas.UploadFileRequestSchema, db: Session) -> schemas.FileSchema:

    # validating given organisation
    organisation_obj = db.query(models.Organisation).get(request_schema.organisation_id)
    if not organisation_obj:
        raise CustomException(*ORGANISATION_DOES_NOT_EXISTS_EXCEPTION)

    # Finding out the file name from given file
    file_name = get_file_name(uploaded_file=request_schema.uploaded_file)

    # validating if file already exists in organisation
    organisation_file_obj = db.query(models.OrganisationFile).filter(
        models.OrganisationFile.id == request_schema.organisation_id,
        models.OrganisationFile.file_name == file_name
    )
    if organisation_file_obj and not request_schema.can_replace_file:
        raise CustomException(*FILE_ALREADY_EXISTS)

    file_uploadable_dir_path = UPLOAD_DIR_BASE_PATH + f"{request_schema.organisation_id}/"
    if not os.path.exists(file_uploadable_dir_path):
        os.makedirs(file_uploadable_dir_path)

    file_path = os.path.join(file_uploadable_dir_path, request_schema.uploaded_file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(request_schema.uploaded_file.file, buffer)

    file_obj = models.OrganisationFile(
        id=get_random_uuid_string_for_primary_key(),
        organisation_id=request_schema.organisation_id, file_name=file_name, file_path=file_path
    )
    db.add(file_obj)
    db.commit()

    return schemas.FileSchema(
        id=file_obj.id, file_name=file_obj.file_name, file_path=file_obj.file_path
    )


def get_file_name(uploaded_file: UploadFile) -> str:
    file_name = ""
    if not file_name:
        raise CustomException(*UNABLE_TO_PROCESS_FILE)
    return file_name
