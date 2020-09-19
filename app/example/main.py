"""Example of data enchancements."""

import enum
import argparse
import dataclasses

from typing import Tuple, List

from sqlalchemy import create_engine

from app.core.data_loader import DataLoaderConfig
from app.core.database import DatabaseConfig
from app.core.mapper import DataJoinConfig, extend_database_records

from app.example.data.data import LOADER_CFG
from app.example.db import DB_URL, DB_KWARGS, DB_CN_ARGS, init_db


class Action(enum.Enum):
    """Script action."""

    init_db = 'init_db'
    run = 'run'

    def __str__(self) -> str:
        """Return string representation of Action."""
        return self.value


@dataclasses.dataclass
class CmdOptions:
    """Command line options."""

    action: Action


def parse_args(args: List[str]) -> CmdOptions:
    """Parse command line arguments into CmdOptions."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--action', '-a',
        action='store',
        type=Action,
        default=Action.init_db,
        choices=list(Action),
        required=True,
    )

    ns = parser.parse_args(args)

    return CmdOptions(action=ns.action)


def initialize():
    """Initialize database."""
    try:
        engine = create_engine(
            DB_URL,
            connect_args=DB_CN_ARGS,
            **DB_KWARGS,
            echo=True,
        )
        init_db(engine)
    finally:
        engine.dispose()


def get_configs() -> Tuple[DataLoaderConfig, DatabaseConfig, DataJoinConfig]:
    """Return configs for processing."""
    db_config = DatabaseConfig(
        db_url=DB_URL,
        table_name='clients',
        db_conn_args=DB_CN_ARGS,
        db_kwargs=DB_KWARGS,
    )

    joiner_cfg = DataJoinConfig(
        search_mappings={
            # CSV column   :  Table column
            'company_egrul': 'egrul',
        },
        update_mapping={
            # CSV column   :  Table column
            'company_phone': 'phone_number',
            'company_address': 'address',
        },
    )

    return LOADER_CFG, db_config, joiner_cfg


def process_data(opts: CmdOptions):
    """Process data in database."""
    if opts.action == Action.init_db:
        initialize()
    elif opts.action == Action.run:
        load_cfg, db_cfg, join_cfg = get_configs()
        extend_database_records(db_cfg, load_cfg, join_cfg)
    else:
        print('Check action enum, you are not added new command here')


if __name__ == "__main__":
    import sys

    opts = parse_args(sys.argv[1:])
    process_data(opts)
