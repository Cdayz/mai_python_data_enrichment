"""Example data load."""

import io
import csv

from pathlib import Path
from typing import Generator

from app.core.data_loader import DataLoaderConfig


def data_fetcher(args: dict) -> io.BytesIO:
    """Read file by path."""
    with args['file_path'].open('rb') as f:
        contents = io.BytesIO(f.read())

    return contents


def data_parser(buf: io.BytesIO) -> Generator[dict, None, None]:
    """Parse csv file as dicts."""
    data = io.StringIO(buf.getvalue().decode('utf-8'))
    reader = csv.DictReader(data, delimiter=';')

    for item in reader:
        for k in item:
            if not item[k]:
                item[k] = None  # type: ignore

        yield item


LOADER_CFG = DataLoaderConfig(
    fetcher_args={'file_path': Path(__file__).parent / Path('data.csv')},
    data_fetcher=data_fetcher,
    data_parser=data_parser,
)
