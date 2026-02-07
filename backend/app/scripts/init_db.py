import os
from app.core.database import execute_script

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_PATH = os.path.join(BASE_DIR, "models", "schema.sql")


def init_database():
    with open(SCHEMA_PATH, "r") as f:
        schema = f.read()
    execute_script(schema)
    print("Database initialized successfully.")


if __name__ == "__main__":
    init_database()
