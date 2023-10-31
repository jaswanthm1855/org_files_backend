import os.path
import shutil
from collections import defaultdict
from typing import List, Tuple

import magic
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


def get_all_organisation_files(db: Session) -> List[schemas.GetOrganisationFilesSchema]:

    org_objs = db.query(models.Organisation).all()

    org_file_objs = db.query(models.OrganisationFile).all()

    org_id_wise_org_file_objs = defaultdict(list)
    for org_file_obj in org_file_objs:
        org_id_wise_org_file_objs[org_file_obj.organisation_id].append(org_file_obj)

    org_files_schemas = []
    for org_obj in org_objs:
        org_files_schemas.append(
            schemas.GetOrganisationFilesSchema(
                id=org_obj.id,
                name=org_obj.name,
                files=org_id_wise_org_file_objs[org_obj.id]
            )
        )
    return org_files_schemas


def get_organisation_files(organisation_id: str, db: Session) -> List[schemas.FileSchema]:
    file_objs = db.query(models.OrganisationFile).filter(
        models.OrganisationFile.organisation_id == organisation_id
    ).all()
    file_schemas = [
        schemas.FileSchema(**file_obj.__dict__) for file_obj in file_objs
    ]
    return file_schemas


def upload_file(
        organisation_id: str, request_schema: schemas.UploadFileRequestSchema, db: Session
) -> schemas.FileSchema:
    # validating given organisation
    organisation_obj = db.query(models.Organisation).get(organisation_id)
    if not organisation_obj:
        raise CustomException(*ORGANISATION_DOES_NOT_EXISTS_EXCEPTION)

    # Finding out the file name from given file
    file_name, file_path_uploaded_to_temp = get_file_name(uploaded_file=request_schema.uploaded_file)

    # validating if file already exists in organisation
    organisation_file_obj = db.query(models.OrganisationFile).filter(
        models.OrganisationFile.organisation_id == organisation_id,
        models.OrganisationFile.file_name == file_name
    ).first()
    if organisation_file_obj:
        if not request_schema.can_replace_file:
            raise CustomException(*FILE_ALREADY_EXISTS)
        else:
            db.query(models.OrganisationFile).filter(
                models.OrganisationFile.organisation_id == organisation_id,
                models.OrganisationFile.file_name == file_name
            ).delete()
            db.commit()
            os.remove(organisation_file_obj.file_path)

    file_uploadable_dir_path = UPLOAD_DIR_BASE_PATH + f"{organisation_id}/"
    if not os.path.exists(file_uploadable_dir_path):
        os.makedirs(file_uploadable_dir_path)

    file_path = os.path.join(file_uploadable_dir_path, request_schema.uploaded_file.filename)
    shutil.move(file_path_uploaded_to_temp, file_path)
    # with open(file_path, "wb") as buffer:
    #     shutil.copyfileobj(request_schema.uploaded_file.file, buffer)

    file_obj = models.OrganisationFile(
        id=get_random_uuid_string_for_primary_key(),
        organisation_id=organisation_id, file_name=file_name, file_path=file_path
    )
    db.add(file_obj)
    db.commit()

    return schemas.FileSchema(
        id=file_obj.id, file_name=file_obj.file_name, file_path=file_obj.file_path
    )


def get_file_name(uploaded_file: UploadFile) -> Tuple[str, str]:
    file_name = uploaded_file.filename

    file_uploadable_dir_path = UPLOAD_DIR_BASE_PATH + f"temp/"
    if not os.path.exists(file_uploadable_dir_path):
        os.makedirs(file_uploadable_dir_path)

    file_path = os.path.join(file_uploadable_dir_path, uploaded_file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)

    magic_obj = magic.Magic(mime=True, uncompress=True)
    file_type_as_per_magic = magic_obj.from_file(file_path)

    file_name_from_file = None
    # We can move all the constants here into plain_constants file
    if uploaded_file.content_type == 'application/pdf' and file_type_as_per_magic == 'application/pdf':
        try:
            import PyPDF2

            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = reader.pages[0].extract_text()
                first_line = text.split('\n')[0]
                file_name_from_file = first_line
        except Exception:
            raise CustomException(*UNABLE_TO_PROCESS_FILE)
    elif (
            uploaded_file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' and
            file_type_as_per_magic == 'text/xml' and file_name.split('.')[-1] == 'docx'
    ):
        try:
            import docx

            doc = docx.Document(file_path)
            first_line = doc.paragraphs[0].text.split('\n')[0]
            file_name_from_file = first_line
        except Exception:
            raise CustomException(*UNABLE_TO_PROCESS_FILE)
    elif uploaded_file.content_type == 'application/vnd.ms-powerpoint' and file_type_as_per_magic == 'application/vnd.ms-powerpoint':
        raise CustomException(*UNABLE_TO_PROCESS_FILE)
    elif uploaded_file.content_type == 'application/vnd.openxmlformats-officedocument.presentationml.presentation' and file_type_as_per_magic == 'text/xml':
        raise CustomException(*UNABLE_TO_PROCESS_FILE)
    else:
        raise CustomException(*UNABLE_TO_PROCESS_FILE)

    if not file_name_from_file:
        raise CustomException(*UNABLE_TO_PROCESS_FILE)

    return file_name_from_file, file_path
