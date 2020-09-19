"""Example of data enchancements."""

import logging

from typing import Tuple

from sqlalchemy import create_engine

from app.core.data_loader import DataLoaderConfig
from app.core.database import DatabaseConfig
from app.core.mapper import DataJoinConfig, extend_database_records

from app.example.data.data import LOADER_CFG
from app.example.db import DB_URL, init_db


logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def initialize() -> Tuple[DataLoaderConfig, DatabaseConfig, DataJoinConfig]:
    """Initialize database and configure processing."""
    db_config = DatabaseConfig(
        db_url=DB_URL,
        table_name='clients',
    )

    try:
        engine = create_engine(
            DB_URL,
            connect_args={'encoding': 'UTF-8', 'nencoding': 'UTF-8'},
            max_identifier_length=128,
        )
        init_db(engine)
    finally:
        engine.dispose()

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


def process_data():
    load_cfg, db_cfg, join_cfg = initialize()
    # extend_database_records(db_cfg, load_cfg, join_cfg)


if __name__ == "__main__":
    process_data()
