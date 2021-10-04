import uuid

from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CommentModel(Base):
    __tablename__ = 'comments'

    id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    video_id = Column(Text(length=36))
    user_id = Column(Text(length=36))
    username = Column(String(1000), nullable=False)
    date = Column(DateTime)
    text = Column(Text(length=6000))
    positive_votes = Column(Integer, nullable=False)
    negative_votes = Column(Integer, nullable=False)
    report = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)

    def __repr__(self):
        return '<Comment {} {} {} {} {} {} {} {} {}>'.format(
            self.id,
            self.video_id,
            self.user_id,
            self.username,
            self.date.timestamp() * 1000,
            self.text,
            self.positive_votes,
            self.negative_votes,
            self.report,
            self.status
        )
