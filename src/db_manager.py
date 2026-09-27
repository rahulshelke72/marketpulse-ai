import duckdb
from config import settings


def get_db_connection():
    """
    Returns an active DuckDB connection.
    Connects to MotherDuck in the cloud or a local file depending on settings.
    """
    if settings.USE_LOCAL_DUCKDB:
        # Connect to local file database
        conn = duckdb.connect(database=str(settings.LOCAL_DB_PATH))
    else:
        # Validate token for cloud connection
        if not settings.MOTHERDUCK_TOKEN:
            raise ValueError(
                "MOTHERDUCK_TOKEN is empty. Set it in .env or switch USE_LOCAL_DUCKDB=true"
            )

        # Connection string for MotherDuck
        connection_uri = f"md:{settings.MOTHERDUCK_DATABASE}?motherduck_token={settings.MOTHERDUCK_TOKEN}"
        conn = duckdb.connect(database=connection_uri)

    return conn


def init_database_schema(conn=None):
    """
    Creates necessary dimension, fact, and audit tables if they don't already exist.
    """
    should_close = False
    if conn is None:
        conn = get_db_connection()
        should_close = True

    try:
        # 1. Watchlist dimension table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS dim_watchlist (
                ticker VARCHAR PRIMARY KEY,
                company_name VARCHAR,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 2. Daily price fact table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS fct_stock_prices (
                ticker VARCHAR,
                trade_date DATE,
                open DOUBLE,
                high DOUBLE,
                low DOUBLE,
                close DOUBLE,
                volume BIGINT,
                ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (ticker, trade_date)
            );
        """)

        # 3. Alert tracking & audit table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS fct_alerts_log (
                alert_id VARCHAR PRIMARY KEY,
                ticker VARCHAR,
                alert_date DATE,
                baseline_price DOUBLE,
                current_price DOUBLE,
                drop_pct DOUBLE,
                gemini_analysis VARCHAR,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    finally:
        if should_close:
            conn.close()