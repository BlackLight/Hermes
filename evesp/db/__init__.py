import os

from stat import S_IRUSR, S_IWUSR
from threading import RLock

from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Db(object):
    """
    Db base class

    @requires sqlalchemy <pip install sqlalchemy>

    Fabio Manganiello, 2015 <blacklight86@gmail.com>
    """

    base = declarative_base()

    # Singleton instance
    __instance = None
    __instance_lock = RLock()

    def __init__(self, db_path):
        """
        Create the db object

        db_path -- Path to the SQLite database
        """

        if not os.path.isfile(db_path):
            open(db_path, 'w').close()
            os.chmod(db_path, S_IRUSR | S_IWUSR)
        else:
            # Enforce mode 0600
            mode = os.stat(db_path).st_mode
            if mode != S_IRUSR | S_IWUSR:
                os.chmod(db_path, S_IRUSR | S_IWUSR)

        self.__import_orm_modules()

        self.engine = create_engine('sqlite:///%s' % db_path)
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)
        self.base.metadata.create_all(self.engine)

    def __import_orm_modules(self):
        """
        Import the table ORM modules.
        This will indirectly create the missing tables on the db as well, for
        the modules extend Db.base before metadata.create_all is invoked
        """

        import sys
        import importlib
        import pkgutil

        return [
            importlib.import_module(__name__ + '.' + name)
            for loader, name, is_pkg in
            pkgutil.walk_packages(sys.modules[__name__].__path__)
        ]

    def close(self):
        self.session.close_all()

    @classmethod
    def get_db(cls, db_path=None):
        """
        Treating db as a singleton
        db_path -- Path to the SQLite database. It has to be passed only on the
        first invocation
        """

        if cls.__instance:
            return cls.__instance

        if db_path is None:
            raise RuntimeError("The db instance has not been initialized yet " +
                               "and no db_path has been passed")

        cls.__instance_lock.acquire()

        try:
            if cls.__instance is None:
                cls.__instance = Db(db_path=db_path)
        finally:
            cls.__instance_lock.release()

        return cls.__instance
