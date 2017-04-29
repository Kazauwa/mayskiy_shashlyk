from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///fires.sqlite')
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class FireSpot (Base):
    __tablename__ = 'fire_location'
    id = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(Float)
    longitude = Column(Float)

    def __init__(self, latitude=None, longitude=None):

        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '{}:{}'.format(self.latitude, self.longitude)


class FireParams(Base):
    __tablename__ = 'fire_params'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ti4channel = Column(Float)
    ti5channel = Column(Float)
    date = Column(DateTime)
    time = Column(DateTime)
    confidence = Column(String(50))
    fire_intens = Column(Float)
    day_night = Column(String(5))
    object_id = Column(Integer, ForeignKey('fire_location.id'))

    def __repr__(self):
        return '{},{},{},{},{},{},{},'.format(self.ti4channel, self.ti5channel, self.date, self.time,
                                              self.confidence, self.fire_intens, self.day_night)


class WindParams(Base):
    __tablename__ = 'wind_params'
    id = Column(Integer, primary_key=True, autoincrement=True)
    speed = Column(Float)
    wind_direction = Column(Float)
    object_id = Column(Integer, ForeignKey('fire_location.id'))

    def __repr__(self):
        return '{},{}'.format(self.speed, self.wind_direction)


class Polygon(Base):
    __table__ = 'polygons'
    id = Column(Integer, primary_key=True, autoincrement=True)


class SpotM2MPolygon(Base):
    __table__ = 'spotm2mpolygon'
    id = Column(Integer, primary_key=True, autoincrement=True)
    polygon_id = Column(Integer, ForeignKey('polygons.id'))
    spot_id = Column(Integer, ForeignKey('fire_location.id'))


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
