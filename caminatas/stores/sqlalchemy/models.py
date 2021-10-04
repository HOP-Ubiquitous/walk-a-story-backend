import uuid
import json

from sqlalchemy import Column, String, Text, DateTime, TypeDecorator
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ArrayType(TypeDecorator):

    def process_literal_param(self, value, dialect):
        pass

    @property
    def python_type(self):
        pass

    impl = String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

    def copy(self):
        return ArrayType(self.impl.length)


class CaminataModel(Base):
    __tablename__ = 'caminatas'

    id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    title = Column(Text(length=100))
    description = Column(Text(length=6000), nullable=False)
    date = Column(DateTime(timezone=True))
    image = Column(Text(length=2048))
    place_id = Column(Text(length=36))
    address = Column(Text(length=300))
    latitude = Column(Text(length=30))
    longitude = Column(Text(length=30))
    user_id = Column(Text(length=36))
    participants = Column(ArrayType())

    def __repr__(self):
        return '<Caminata {} {} {} {} {} {} {} {} {} {} {}>'.format(
            self.id,
            self.title,
            self.description,
            str(self.date),
            self.image,
            self.place_id,
            self.address,
            self.latitude,
            self.longitude,
            self.user_id,
            self.participants
        )
