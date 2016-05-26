from datetime import datetime

from . import Db
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey


class FileSystemResourceEvent(Db.base):
    """
    Map a filesystem resource history item object to the database

    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    __tablename__ = 'fs_resource_event'
    id = Column(Integer, primary_key=True)
    path = Column(String, ForeignKey('fs_resource.path'))
    mode = Column(Integer, nullable=False)
    diff = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    last_updated_at = Column(
        DateTime, nullable=False,
        default=datetime.now,
        onupdate=datetime.now
    )

# vim:sw=4:ts=4:et:
