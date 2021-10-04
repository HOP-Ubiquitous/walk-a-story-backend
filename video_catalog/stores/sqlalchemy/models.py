import datetime
import uuid

from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class VideoModel(Base):
    __tablename__ = 'videos'

    id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    g_path = Column(String, nullable=False)
    public_url = Column(String, nullable=False)
    file_public = Column(Boolean)
    analysis_url = Column(String)
    file_status = Column(Integer)
    user_id = Column(Text(length=36))
    place_id = Column(Text(length=36))
    title = Column(Text(length=100))
    description = Column(Text(length=6000))
    username = Column(String, nullable=False)
    creation_date = Column(DateTime, default=datetime.datetime.now)
    latitude = Column(Text(length=30))
    longitude = Column(Text(length=30))
    positive_votes = Column(Integer)
    negative_votes = Column(Integer)
    reports = Column(Integer)

    def __repr__(self):
        return '<Video {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}>'.format(
            self.id,
            self.g_path,
            self.public_url,
            self.analysis_url,
            self.file_public,
            self.file_status,
            self.user_id,
            self.place_id,
            self.title,
            self.description,
            self.username,
            self.creation_date.timestamp() * 1000,
            self.latitude,
            self.longitude,
            self.positive_votes,
            self.negative_votes,
            self.reports
        )
