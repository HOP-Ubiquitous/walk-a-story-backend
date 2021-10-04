import uuid

from sqlalchemy import Column, Text, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class CityModel(Base):
    __tablename__ = 'city'

    id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    name = Column(Text(length=100), unique=True)
    points_of_interest = relationship("PointOfInterestModel", backref='city')

    def __repr__(self):
        return '<City {} {}>'.format(
            self.id,
            self.name,
            self.points_of_interest
        )


class PointOfInterestModel(Base):
    __tablename__ = 'pointofinterest'

    id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    name = Column(Text(length=100))
    city_id = Column(Text(length=36), ForeignKey('city.id'))
    latitude = Column(Text(length=30))
    longitude = Column(Text(length=30))

    def __repr__(self):
        return '<PointOfInterest {} {} {} {} {}>'.format(
            self.id,
            self.name,
            self.city_id,
            self.latitude,
            self.longitude
        )
