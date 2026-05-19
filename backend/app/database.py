from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import Config, config


class Database:
    """
    Initialize an instance of a Database class and create a database connection link.
    """

    def __init__(self, config: Config) -> None:
        self.__engine = create_async_engine(
            config.db_url,
            connect_args={
                "ssl": "require",
                "server_settings": {"channel_binding": "require"},
            },
        )
        self.__session_factory = async_sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )

    @asynccontextmanager
    async def get_db_session(self):
        """
        Context manager that yields a database connection session.
        Raises RuntimeError if it encounters a connection error or a timeout error.
        Automatically handles closing the session.
        """
        session = self.__session_factory()
        try:
            yield session
            await session.commit()
        except ConnectionError as err:
            await session.rollback()
            raise RuntimeError(f"There was a problem connecting to the database: {err}")
        except TimeoutError:
            await session.rollback()
            raise RuntimeError("Database connection timed out.")
        finally:
            await session.close()


db = Database(config)
