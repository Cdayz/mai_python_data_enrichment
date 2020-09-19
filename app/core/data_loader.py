"""Data loader."""

import io
import dataclasses

from typing import Generator, Callable, Any


@dataclasses.dataclass
class DataLoaderConfig:
    """Data load config."""

    fetcher_args: Any
    data_fetcher: Callable[..., io.BytesIO]
    data_parser: Callable[[io.BytesIO], Generator[dict, None, None]]


def fetch_data_by_config(config: DataLoaderConfig) -> Generator[dict, None, None]:
    """Fetch data by data loader config and create generator which yields data."""
    file_bytes = config.data_fetcher(config.fetcher_args)

    # NOTE: mypy think that data_parser function receives a self argument, but it not work so
    for item in config.data_parser(file_bytes):  # type: ignore
        yield item
