from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base
import datetime


class PTSession(Base):
    """ PT session """

    __tablename__ = "pt_session"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(250), nullable=False)
    trainer_id = Column(String(250), nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    duration_hours = Column(Float, nullable=False)
    user_name = Column(String(250), nullable=False)
    user_height = Column(Float, nullable=False)
    user_weight = Column(Float, nullable=False)
    start_time = Column(String(100), nullable=False)
    user_address = Column(String(250), nullable=False)
    trace_id = Column(String(250), nullable=False)

    def __init__(self, user_id, user_name, user_height, user_weight, user_address, trainer_id,duration_hours,start_time,timestamp, trace_id):
        """ Initializes a pt session request """
        self.user_id = user_id
        self.timestamp = datetime.datetime.now()
        self.date_created = datetime.datetime.now()  # Sets the date/time record is created
        self.duration_hours = duration_hours
        self.user_name = user_name
        self.user_height = user_height
        self.user_weight = user_weight
        self.trainer_id = trainer_id
        self.user_address = user_address
        self.start_time = start_time
        self.trace_id = trace_id

    def to_dict(self):
        """ Dictionary Representation of a pt session """
        dict = {}
        dict['id'] = self.id
        dict['duration_hours'] = self.duration_hours
        dict['start_time'] = self.start_time
        dict['user_info'] = {}
        dict['user_info']['user_id'] = self.user_id
        dict['user_info']['user_name'] = self.user_name
        dict['user_info']['user_height'] = self.user_height
        dict['user_info']['user_weight'] = self.user_weight
        dict['user_info']['user_address'] = self.user_address
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created
        dict['trainer_id'] = self.trainer_id
        dict['trace_id'] = self.trace_id

        return dict

