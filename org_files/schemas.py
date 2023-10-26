from typing import Dict, List

from fastapi import UploadFile
from pydantic import BaseModel

from constants import enums


class BaseResponseSchema(BaseModel):
    status: enums.StatusType
    message: str
    data: Dict = {}


class OrganisationSchema(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True


class GetOrganisationsSuccessSchema(BaseResponseSchema):
    data: List[OrganisationSchema]


class FileSchema(BaseModel):
    id: str
    file_name: str
    file_path: str


class GetFilesSuccessSchema(BaseResponseSchema):
    data: List[FileSchema]


class UploadFileRequestSchema(BaseModel):
    organisation_id: str
    uploaded_file: UploadFile
    can_replace_file: bool = False


class UploadFileSuccessSchema(BaseResponseSchema):
    data: FileSchema
