import sqlalchemy as sa

NAMING_CONVENTION = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = sa.MetaData(naming_convention=NAMING_CONVENTION)

information_table = sa.Table(
    'clients', metadata,
    sa.Column('client_id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(100), nullable=False),
    sa.Column('egrul', sa.String(50), nullable=False),
    sa.Column('phone_number', sa.String(80), nullable=True),
    sa.Column('address', sa.String(300), nullable=True),
)
