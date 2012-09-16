# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm


Session = orm.scoped_session(orm.sessionmaker())
Base = declarative_base()
# Metadata = Base.metadata

from vehicles import *


def connect(uri, encoding='utf8'):
    engine = create_engine(uri, encoding=encoding)
    Session.configure(bind=engine)
    Base.metadata.bind = engine
