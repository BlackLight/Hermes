from datetime import datetime

from . import Db
from sqlalchemy import Column, String, DateTime


class FileSystemResource(Db.base):
    """
    Map a filesystem resource object to the database

    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    __tablename__ = 'fs_resource'
    path = Column(String, primary_key=True)
    orig_content = Column(String)
    content = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    last_updated_at = Column(
        DateTime, nullable=False,
        default=datetime.now,
        onupdate=datetime.now
    )

# vim:sw=4:ts=4:et:
