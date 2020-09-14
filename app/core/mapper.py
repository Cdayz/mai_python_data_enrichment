import dataclasses

from typing import Mapping, List

from app.core.data_loader import DataLoaderConfig, fetch_data_by_config
from app.core.database import DatabaseConfig, get_database_by_config


@dataclasses.dataclass
class DataJoinConfig:
    search_mappings: Mapping[str, str]
    update_mapping: Mapping[str, str]


def extend_database_records(
    db_cfg: DatabaseConfig,
    data_load_cfg: DataLoaderConfig,
    join_cfg: DataJoinConfig,
):
    data: List[dict] = fetch_data_by_config(data_load_cfg)

    with get_database_by_config(db_cfg) as database:
        for item in data:
            item_pk = {}
            update_data = {}

            for field, value in item.values():
                if field in join_cfg.search_mappings:
                    item_pk[join_cfg.search_mappings[field]] = value
                elif field in join_cfg.update_mapping:
                    update_data[join_cfg.update_mapping[field]] = value

                if item_pk in database:
                    database.update_item(item_pk, update_data)
