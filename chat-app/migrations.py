from sqlalchemy import inspect, text
from db import engine, Base
import models  # IMPORTANT: load models


def migrate():
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    # 1️⃣ Create missing tables
    for table in Base.metadata.tables.values():
        if table.name not in existing_tables:
            print(f"Creating table: {table.name}")
            table.create(bind=engine)

    # 2️⃣ Add missing columns (SAFE MODE)
    for table in Base.metadata.tables.values():
        if table.name in existing_tables:
            existing_columns = {
                col["name"] for col in inspector.get_columns(table.name)
            }

            for column in table.columns:
                if column.name not in existing_columns:
                    ddl = (
                        f"ALTER TABLE {table.name} "
                        f"ADD COLUMN {column.name} "
                        f"{column.type.compile(engine.dialect)}"
                    )

                    print(f"Adding column: {table.name}.{column.name}")

                    with engine.begin() as conn:
                        conn.execute(text(ddl))


if __name__ == "__main__":
    migrate()
    print("✅ Migration completed successfully")
