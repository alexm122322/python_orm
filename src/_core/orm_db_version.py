from .ddl.model import Model
from .ddl.column import Column
from .ddl.column_types.integer import Integer


class OrmDBVersion(Model):
    """The table for read/write the database version. 
    Migration purposes only.

    Args:
        value: The field of the database version value.
    """
    __tablename__ = 'orm_db_version'
    value = Column(name='value', type=Integer(), nullable=False)
