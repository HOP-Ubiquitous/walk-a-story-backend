import uuid

from sqlalchemy import Column, String, Text, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'users'

    id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    password = Column(String(100), nullable=False)
    username = Column(String(1000), nullable=False)
    email = Column(String(1000), nullable=False)
    name = Column(String(1000), nullable=False)
    admin = Column(Boolean)
    birth_date = Column(DateTime)

    def __repr__(self):
        return '<User {} {} {} {} {} {}>'.format(
            self.id, self.username, self.email, self.name, self.admin, self.birth_date.timestamp() * 1000
        )
