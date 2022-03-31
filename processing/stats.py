from sqlalchemy import Column, Float, Integer, DateTime 
from base import Base 
class Stats(Base): 
    """ Processing Statistics """ 
 
    __tablename__ = "stats" 
 
    id = Column(Integer, primary_key=True) 
    num_membership = Column(Integer, nullable=False) 
    num_pt_session = Column(Integer, nullable=False) 
    max_height = Column(Float, nullable=True) 
    max_weight = Column(Float, nullable=True) 
    last_updated = Column(DateTime, nullable=False) 
 
    def __init__(self, num_membership, num_pt_session, max_height, max_weight,last_updated): 
        """ Initializes a processing statistics objet """ 
        self.num_membership = num_membership 
        self.num_pt_session = num_pt_session 
        self.max_height = max_height 
        self.max_weight = max_weight 
        self.last_updated = last_updated 
 
    def to_dict(self): 
        """ Dictionary Representation of a statistics """ 
        dict = {} 
        dict['num_membership'] = self.num_membership 
        dict['num_pt_session'] = self.num_pt_session 
        dict['max_height'] = self.max_height 
        dict['max_weight'] = self.max_weight 
        dict['last_updated'] = self.last_updated.strftime("%Y-%m-%dT%H:%M:%SZ") 
 
        return dict