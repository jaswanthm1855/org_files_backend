from starlette import status

from constants import enums

ORGANISATION_DOES_NOT_EXISTS_EXCEPTION = (
    status.HTTP_404_NOT_FOUND,
    enums.StatusType.ERROR.value,
    "Organisation does not exists"
)

FILE_ALREADY_EXISTS = (
    status.HTTP_400_BAD_REQUEST,
    enums.StatusType.ERROR.value,
    "File already exists"
)

UNABLE_TO_PROCESS_FILE = (
    status.HTTP_400_BAD_REQUEST,
    enums.StatusType.ERROR.value,
    "We are unable to process the file"
)

FILE_NOT_ACCEPTED_FOR_PROCESSING = (
    status.HTTP_400_BAD_REQUEST,
    enums.StatusType.ERROR.value,
    "We are not accepting these files for processing"

)
