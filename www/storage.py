from sqlalchemy import (MetaData, Table, Column, Integer, DateTime, ForeignKey, Unicode)

metadata = MetaData()

update_table = Table(
    'update',
    metadata,
    Column('id', Integer, primary_key = True),
    Column('time', DateTime),
    Column('total_online', Integer)
)