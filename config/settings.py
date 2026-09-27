import os
from pathlib import Path
from dotenv import load_dotenv

# Locate and load the root .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

MOTHERDUCK_TOKEN = os.getenv("MOTHERDUCK_TOKEN", "").strip()
MOTHERDUCK_DATABASE = os.getenv("MOTHERDUCK_DATABASE", "marketplus_db").strip()
USE_LOCAL_DUCKDB = os.getenv("USE_LOCAL_DUCKDB", "false").lower() == "true"

# Local storage path inside data/ folder
LOCAL_DB_PATH = BASE_DIR / "data" / "marketplus.duckdb"