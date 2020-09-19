"""Database initialization."""

from sqlalchemy.engine import Engine
from sqlalchemy import select, insert, update

from app.example.db.info_table import information_table, metadata


def row_exists(db: Engine, pk: int):
    """Check that row exits."""
    query = select([information_table.c.client_id]).where(
        information_table.c.client_id == pk,
    )

    client_id = db.execute(query)

    if client_id is not None:
        return True

    return False


def insert_row(db: Engine, row: dict):
    """Insert row to database."""
    query = insert(information_table).values(
        **row,
    ).returning(information_table.c.client_id)

    inserted_id = db.execute(query)

    return inserted_id


def update_row(db: Engine, row: dict):
    """Update row in database."""
    query = update(information_table).where(
        information_table.c.client_id == row['client_id'],
    ).values(**row).returning(information_table.c.client_id)

    updated_id = db.execute(query)

    return updated_id


def update_or_create(db: Engine, row: dict):
    """Update or create row in database."""
    if row_exists(db, row['client_id']):
        uid = update_row(db, row)
        created = False
    else:
        uid = insert_row(db, row)
        created = True

    return uid, created


def init_db(db: Engine):
    """Initialize example database."""
    metadata.create_all(
        db,
        tables=[information_table],
        checkfirst=True,
    )

    info = [
        {
            "client_id": 1,
            "name": "Jet Brains",
            "egurl": "JB-EGURL-1",
            "phone_number": None,
            "address": None,
        },
        {
            "client_id": 2,
            "name": "Mail.ru",
            "egurl": "MRG-EGURL-1",
            "phone_number": "Shitty MRG",
            "address": None,
        },
        {
            "client_id": 3,
            "name": "Yandex",
            "egurl": "YA-EGURL-1",
            "phone_number": None,
            "address": "Yandex everywhere",
        },
        {
            "client_id": 4,
            "name": "Telegram",
            "egurl": "TG-EGURL-1",
            "phone_number": "tg-number",
            "address": "Telegram everywhere",
        },
    ]

    for row in info:
        uid, created = update_or_create(db, row)
