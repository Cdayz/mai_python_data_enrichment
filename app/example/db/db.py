"""Database url."""

import os
from urllib.parse import quote

DB_SCHEME = os.environ['DB_SCHEME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_DSN = os.environ['DB_DSN']

# Connection URL
DB_URL = f'{DB_SCHEME}://{quote(DB_USER)}:{quote(DB_PASSWORD)}@{DB_DSN}'

# DB_CN_ARGS = {'encoding': 'UTF-8', 'nencoding': 'UTF-8'}
# DB_KWARGS = {'max_identifier_length': 128}

DB_CN_ARGS: dict = {}
DB_KWARGS: dict = {}
