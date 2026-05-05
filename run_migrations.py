import asyncio
from pathlib import Path

import asyncpg

from db import DbClient
from dependencies import get_db_client

MIGRATIONS_DIR = "./migrations"
CHECK_MIGRATION_QUERY = """SELECT * FROM _migrations WHERE name = $1"""
INSERT_MIGRATION_QUERY = """INSERT INTO _migrations (name) VALUES ($1)"""
CREATE_MIGRATIONS_TABLE_FILE_NAME = "000_create_migrations"
CREATE_MIGRATONS_TABLE_FILE_PATH = (
    f"{MIGRATIONS_DIR}/{CREATE_MIGRATIONS_TABLE_FILE_NAME}.sql"
)


async def run():
    db_client: DbClient = get_db_client()
    async with db_client.get_db_conn() as db:
        try:
            await db.fetch(CHECK_MIGRATION_QUERY, CREATE_MIGRATIONS_TABLE_FILE_NAME)
        except asyncpg.exceptions.UndefinedTableError:
            print("Migrations table does not exist! Creating table...")
            create_migrations_table_file = Path(CREATE_MIGRATONS_TABLE_FILE_PATH)
            await db.execute(create_migrations_table_file.read_text())

        for file in sorted(Path(MIGRATIONS_DIR).glob("*.sql")):
            migration_name, migration_query = file.stem, file.read_text()
            try:
                if migration_name == CREATE_MIGRATIONS_TABLE_FILE_NAME:
                    continue

                result = await db.fetch(CHECK_MIGRATION_QUERY, migration_name)
                if len(result) != 0:
                    print(f"Migration {migration_name} already applied, skipping...")
                    continue

                async with db.transaction():
                    await db.execute(migration_query)
                    await db.execute(INSERT_MIGRATION_QUERY, migration_name)
                    print(f"{migration_name} applied")
            except Exception as err:
                print(f"Could not execute migration {migration_name}, err is {err}")


asyncio.run(run())
