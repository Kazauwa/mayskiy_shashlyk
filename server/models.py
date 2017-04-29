from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///fires.sqlite')
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class FireSpot(Base):
    __tablename__ = 'fire_location'
    id = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(Float)
    longitude = Column(Float)
    date_time = Column(DateTime)
    is_day = Column(Boolean)

    def __repr__(self):
        return '{}:{}'.format(self.latitude, self.longitude)


class FireParams(Base):
    __tablename__ = 'fire_params'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ti4channel = Column(Float)
    ti5channel = Column(Float)
    confidence = Column(String(50))
    fire_intens = Column(Float)
    object_id = Column(Integer, ForeignKey('fire_location.id'))

    def __repr__(self):
        return '{},{},{},{},{},{},{},'.format(self.ti4channel, self.ti5channel, self.date, self.time,
                                              self.confidence, self.fire_intens, self.day_night)


class WeatherParams(Base):
    __tablename__ = 'wind_params'
    id = Column(Integer, primary_key=True, autoincrement=True)
    object_id = Column(Integer, ForeignKey('fire_location.id'))
    speed = Column(Float)
    wind_direction = Column(Float)
    temperature = Column(Float)
    humidity = Column(Integer)
    is_raining = Column(Boolean)

    def __repr__(self):
        return '{},{}'.format(self.speed, self.wind_direction)


class Polygon(Base):
    __tablename__ = 'polygons'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50))


class SpotM2MPolygon(Base):
    __tablename__ = 'spotm2mpolygon'
    id = Column(Integer, primary_key=True, autoincrement=True)
    polygon_id = Column(Integer, ForeignKey('polygons.id'))
    spot_id = Column(Integer, ForeignKey('fire_location.id'))


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
