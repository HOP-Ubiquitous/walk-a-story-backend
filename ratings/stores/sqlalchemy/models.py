import uuid

from sqlalchemy import Column, Text, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RatingModel(Base):
    __tablename__ = 'ratings'

    id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    associated_id = Column(Text(length=36))
    associated_type = Column(Text(length=10))
    user_id = Column(Text(length=36))
    rating_type = Column(Text(length=10))
    date = Column(DateTime)
    value = Column(Integer, nullable=False)

    def __repr__(self):
        return '<Rating {} {} {} {} {} {} {}>'.format(
            self.id,
            self.associated_id,
            self.associated_type,
            self.user_id,
            self.rating_type,
            str(self.date),
            self.value
        )
