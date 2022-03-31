from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base
import datetime


class GymMember(Base):
    """ Gym Member """

    __tablename__ = "gym_member"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(250), nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    membership_months = Column(Integer, nullable=False)
    user_name = Column(String(250), nullable=False)
    user_height = Column(Float, nullable=False)
    user_weight = Column(Float, nullable=False)
    start_date = Column(String(100), nullable=False)
    gym_address = Column(String(250), nullable=False)
    user_address = Column(String(250), nullable=False)
    trace_id = Column(String(250), nullable=False)

    def __init__(self, user_id, user_name, user_height, user_weight, user_address, gym_address,membership_months,start_date,timestamp, trace_id):
        """ Initializes a gym membership request """
        self.user_id = user_id
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()  # Sets the date/time record is created
        self.membership_months = membership_months
        self.user_name = user_name
        self.user_height = user_height
        self.user_weight = user_weight
        self.gym_address = gym_address
        self.user_address = user_address
        self.start_date = start_date
        self.trace_id = trace_id

    def to_dict(self):
        """ Dictionary Representation of a gym membership """
        dict = {}
        dict['id'] = self.id
        dict['membership_months'] = self.membership_months
        dict['start_date'] = self.start_date
        dict['user_info'] = {}
        dict['user_info']['user_id'] = self.user_id
        dict['user_info']['user_name'] = self.user_name
        dict['user_info']['user_height'] = self.user_height
        dict['user_info']['user_weight'] = self.user_weight
        dict['user_info']['user_address'] = self.user_address
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created
        dict['gym_address'] = self.gym_address
        dict['trace_id'] = self.trace_id

        return dict

