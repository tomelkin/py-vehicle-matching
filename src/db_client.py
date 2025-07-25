import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Any, Tuple, List, Dict, Optional

class DatabaseClient:
    """
    Simple database client for querying PostgreSQL using psycopg2.
    """
    def __init__(self, dsn: Optional[str] = None):
        """
        Initialize the DatabaseClient.
        Args:
            dsn: The PostgreSQL DSN string. If not provided, loads from environment variables.
        """
        load_dotenv()
        if dsn is not None:
            self.dsn = dsn
        else:
            self.dsn = (
                f"host={os.getenv('PGHOST', 'localhost')} "
                f"dbname={os.getenv('PGDATABASE', 'autograb')} "
                f"user={os.getenv('PGUSER', 'autograb_user')} "
                f"password={os.getenv('PGPASSWORD', 'autograb_password')} "
                f"port={os.getenv('PGPORT', 5432)}"
            )

    def query(self, sql: str, params: Tuple[Any, ...] = ()) -> List[Dict[str, Any]]:
        """
        Execute a SQL query and return the results as a list of dictionaries.
        Args:
            sql: The SQL query string
            params: Query parameters as a tuple
        Returns:
            List of result rows as dictionaries
        """
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, params)
                return cur.fetchall() 