import pytest
from django.db import connections


@pytest.mark.django_db
class TestDatabaseConnection:
    def test_database_connection(self):
        """Verify SQLite connection works"""
        db_conn = connections["default"]
        try:
            c = db_conn.cursor()
            c.execute("SELECT 1")
            result = c.fetchone()
            assert result == (1,)
        finally:
            c.close()
