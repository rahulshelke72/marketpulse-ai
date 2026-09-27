from src.db_manager import get_db_connection, init_database_schema


def test_connection():
    print("Connecting to database...")
    conn = get_db_connection()

    # 1. Run a basic query
    result = conn.execute("SELECT 1 AS connection_test;").fetchall()
    print("Connection successful! Test query result:", result)

    # 2. Run schema initialization
    print("Creating tables if they do not exist...")
    init_database_schema(conn)
    print("Tables initialized.")

    # 3. Show all tables in the database
    tables = conn.execute("SHOW TABLES;").df()
    print("\nAvailable tables in database:")
    print(tables)

    conn.close()


if __name__ == "__main__":
    test_connection()