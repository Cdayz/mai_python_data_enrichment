import io
import requests
import dataclasses

from typing import Generator, Callable


@dataclasses.dataclass
class DataLoaderConfig:
    resource_url: str
    data_parser: Callable[[io.BytesIO], Generator[dict, None, None]]


def download_file(url: str) -> io.BytesIO:
    response = requests.get(url, streaming=True)
    return io.BytesIO(response.content)


def fetch_data_by_config(config: DataLoaderConfig) -> Generator[dict, None, None]:
    file_bytes = download_file(config.resource_url)

    for item in config.data_parser(file_bytes):
        yield item
