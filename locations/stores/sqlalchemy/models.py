import uuid

from sqlalchemy import Column, String, DateTime, JSON, Boolean, Float, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class LocationModel(Base):
    __tablename__ = 'locations'

    id = Column('id', String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    is_active = Column(Boolean)
    type = Column(String(length=100), nullable=False)
    subtype = Column(String(length=100), nullable=False)
    title = Column(String(length=100), nullable=False)
    description = Column(String(length=6000))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    workers = Column(JSON)
    owner_user_id = Column(String(length=36))
    main_video_id = Column(String(length=36))
    creation_date = Column(DateTime(timezone=True))

    def __repr__(self):
        return '<Location {} {} {} {} {} {} {} {} {} {} {} {}>'.format(
            self.id,
            self.is_active,
            self.type,
            self.subtype,
            self.title,
            self.description,
            self.latitude,
            self.longitude,
            self.longitude,
            self.workers,
            self.owner_user_id,
            self.main_video_id,
            str(self.creation_date),
        )
