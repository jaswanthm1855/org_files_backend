from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base, declarative_mixin, declared_attr

from utils.get_random_id_string import get_random_uuid_string_for_primary_key

Base = declarative_base()


@declarative_mixin
class BaseMixin:
    __abstract__ = True

    id = Column(
        String(50), primary_key=True, index=True, nullable=False, unique=True,
        default=get_random_uuid_string_for_primary_key
    )

    @declared_attr
    def __tablename__(cls):
        given_table_name = cls.__name__
        converted_table_name = ''.join(
            ['_' + char.lower() if char.isupper() else char for char in given_table_name]
        ).lstrip('_')
        converted_table_name += 's'
        return converted_table_name
