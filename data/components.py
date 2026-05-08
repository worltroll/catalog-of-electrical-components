import sqlalchemy
from .db_session import SqlAlchemyBase


# Capacitor, Resistor, Transistor, Diod, Button, Drossel
class Component(SqlAlchemyBase):
    __tablename__ = 'components'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    about = sqlalchemy.Column(sqlalchemy.String)
    tool = sqlalchemy.Column(sqlalchemy.String)
