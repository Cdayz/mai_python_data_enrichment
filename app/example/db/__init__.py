"""Database config."""

from .init_db import init_db
from .db import DB_URL


__all__ = (
    'DB_URL',
    'init_db',
)
