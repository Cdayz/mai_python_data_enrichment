"""Database url."""

import os
from urllib.parse import quote

DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_DSN = os.environ['DB_DSN']

DB_URL = f'oracle+cx_oracle://{quote(DB_USER)}:{quote(DB_PASSWORD)}@{DB_DSN}'
