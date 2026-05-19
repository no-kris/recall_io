from sqlalchemy import text

from app.database import db


def test_db_connection_ping():
    """
    Ping the database to see if a connection can be made.
    """
    with db.get_db_session() as session:
        result = session.execute(text("SELECT 1")).scalar()
        assert result == 1
