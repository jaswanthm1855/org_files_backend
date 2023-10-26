import uuid


def get_random_uuid_string_for_primary_key() -> str:
    uuid_string = get_random_uuid_string()
    simple_uuid_string = uuid_string.replace('-', '')
    return simple_uuid_string


def get_random_uuid_string() -> str:
    return str(uuid.uuid4())
