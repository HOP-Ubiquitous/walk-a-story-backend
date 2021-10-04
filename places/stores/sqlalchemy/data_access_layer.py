from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from places.stores.sqlalchemy.models import Base


class DataAccessLayer:

    def __init__(self, conn_string):
        self.engine = None
        self.session = None
        self.conn_string = conn_string

    def connect(self):
        self.engine = create_engine(self.conn_string, connect_args={'check_same_thread': False}, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
