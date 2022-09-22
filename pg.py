from sqlalchemy import create_engine, select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

import random
import pygame

engine = create_engine('postgresql+psycopg2://develop:}c%4Z>n~M<3p:Em\@localhost/football')
Base = automap_base()
Base.prepare(engine, reflect=True,schema='core')
Event=Base.classes.events
Session = sessionmaker(bind=engine)
session = Session()
n = random.randrange(0, 1000000, 2000)
sample_id = session.query(Event.globalgameid).limit(1).offset(n).first()[0]
events = session.query(Event).where(Event.globalgameid==sample_id).all()
session.invalidate()
sorted_events = sorted(events, key=lambda e: (e.expandedminute*60+e.second,e.globaleventid))

screen_size = 500
screen = pygame.display.set_mode((screen_size, screen_size))

