import sqlalchemy as sa
from sqlalchemy import MetaData, UUID
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base(object):
    __name__: str
    metadata: MetaData

    id = sa.Column(
        UUID(as_uuid=True),
        primary_key=True
    )
