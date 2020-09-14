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
    table_name: str


class Database:
    def __init__(
        self,
        session: Session,
        engine: Engine,
        table_name: str,
    ):
        self.session = session
        self.engine = engine
        self.table = self.reflect_table(table_name)

    def reflect_table(self, table_name: str) -> Table:
        Base = automap_base()
        Base.prepare(self.engine, reflect=True)
        table = getattr(Base.classes, table_name)

        return table

    def update_item(self, item_pk: dict, update_fields: dict):
        db_row = self.session.query(self.table).filter_by(**item_pk).one()

        for field, value in update_fields.items():
            setattr(db_row, field, value)

        self.session.add(db_row)

    def __contains__(self, item_pk: dict):
        try:
            self.session.query(self.table).filter_by(**item_pk).one()
        except NoResultFound:
            return False
        except MultipleResultsFound:
            raise

        return True


@contextlib.contextmanager
def get_database_by_config(config: DatabaseConfig) -> Iterator[Database]:
    engine = create_engine(config.db_url, encoding='utf-8')
    session = Session(engine)

    try:
        yield Database(engine, session, table_name=config.table_name)
        session.commit()
    except Exception as e:
        session.rollback()
        log.exception(e)
        raise e
    finally:
        session.close()
        engine.dispose()
