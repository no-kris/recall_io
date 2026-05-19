from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import Config, config


class Database:
    """
    Initialize an instance of a Database class and create a database connection link.
    """

    def __init__(self, config: Config) -> None:
        self.__engine = create_engine(config.db_url)
        self.__session_factory = sessionmaker(bind=self.__engine)

    @contextmanager
    def get_db_session(self):
        """
        Context manager that yields a database connection session.
        Raises RuntimeError if it encounters a connection error or a timeout error.
        Automatically handles closing the session.
        """
        session = self.__session_factory()
        try:
            yield session
            session.commit()
        except ConnectionError as err:
            session.rollback()
            raise RuntimeError(f"There was a problem connecting to the database: {err}")
        except TimeoutError:
            session.rollback()
            raise RuntimeError("Database connection timed out.")
        finally:
            session.close()


db = Database(config)
