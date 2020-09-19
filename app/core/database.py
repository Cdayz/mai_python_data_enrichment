"""Database wrapper."""

import logging
import contextlib
import dataclasses

from sqlalchemy import Table
from sqlalchemy import create_engine

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from sqlalchemy.engine import Engine
from sqlalchemy.ext.automap import automap_base

from typing import Iterator


log = logging.getLogger(__name__)


@dataclasses.dataclass
class DatabaseConfig:
    """Database configuration."""

    db_url: str
    db_conn_args: dict
    db_kwargs: dict
    table_name: str


class Database:
    """Wrapper around database which uses sqlalchemy reflection."""

    def __init__(
        self,
        session: Session,
        engine: Engine,
        table_name: str,
    ):
        """Initialize wrapper with database engine and session."""
        self.session = session
        self.engine = engine
        self.table = self.reflect_table(table_name)

    def reflect_table(self, table_name: str) -> Table:
        """Get table from database through sqlalchemy reflection."""
        Base = automap_base()
        Base.prepare(self.engine, reflect=True)
        table = getattr(Base.classes, table_name)

        return table

    def update_item(self, item_pk: dict, update_fields: dict):
        """Update item in database by pk with update_fields."""
        db_row = self.session.query(self.table).filter_by(**item_pk).one()

        for field, value in update_fields.items():
            setattr(db_row, field, value)

        self.session.add(db_row)

    def __contains__(self, item_pk: dict):
        """Check that element by given pk exists in database."""
        try:
            self.session.query(self.table).filter_by(**item_pk).one()
        except NoResultFound:
            return False
        except MultipleResultsFound:
            raise

        return True


@contextlib.contextmanager
def get_database_by_config(config: DatabaseConfig) -> Iterator[Database]:
    """Context manager which creates database wrapper."""
    engine = create_engine(
        config.db_url,
        connect_args=config.db_conn_args,
        **config.db_kwargs,
    )
    session = Session(engine)

    try:
        yield Database(session, engine, table_name=config.table_name)
        session.commit()
    except Exception as e:
        session.rollback()
        log.exception(e)
        raise e
    finally:
        session.close()
        engine.dispose()
