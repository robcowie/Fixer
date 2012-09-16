# -*- coding: utf-8 -*-

from sqlalchemy import orm
from sqlalchemy import Boolean, Column, Integer, Unicode, ForeignKey


from __init__ import Base


class VehicleCategory(Base):
    __tablename__ = 'vehicle_categories'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)


class Vehicle(Base):
    __tablename__ = 'vehicles'

    id  = Column(Integer, primary_key=True)
    reg = Column(Unicode(40))
    category_id = Column(Integer, ForeignKey('vehicle_categories.id'), nullable=False)

    category = orm.relationship('VehicleCategory', uselist=False)
