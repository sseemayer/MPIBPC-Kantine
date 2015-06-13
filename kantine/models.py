from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from kantine.database import Base


class Meal(Base):
    __tablename__ = 'meals'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    name = Column(String(512))
    name_en = Column(String(512))
    mealtype = Column(String(20))



