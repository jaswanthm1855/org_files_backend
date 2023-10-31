from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref

from models.base import Base, BaseMixin


class Organisation(Base, BaseMixin):
    name = Column(String(100), unique=True, nullable=False)

    def __str__(self):
        return f"<Organisation: {self.name}>"


class OrganisationFile(Base, BaseMixin):
    organisation_id = Column(
        String(50), ForeignKey(Organisation.id, ondelete='CASCADE'), nullable=False)
    organisation = relationship(
        Organisation, foreign_keys=[organisation_id], backref=backref("files")
    )
    file_name = Column(String(100), nullable=False)
    file_path = Column(String(300), nullable=False)

    __table_args__ = (
        UniqueConstraint('organisation_id', 'file_name', name='org_file_name_uc'),
    )

    def __str__(self):
        return f"<OrganisationFile: {self.file_name} of organisation {self.organisation.name}>"
