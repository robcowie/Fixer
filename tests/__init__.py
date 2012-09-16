# -*- coding: utf-8 -*-

from fixer import Fixture


# class VehicleCategories(object):

#     class VehicleCategory_car(Fixture):
#         name = u'Car'
#         slug = u'car'

#     class VehicleCategory_motorbike(Fixture):
#         name = u'Motorbike'
#         slug = u'motorbike'

#     class VehicleCategory_bike(Fixture):
#         name = u'Bike'
#         slug = u'bike'


# class Vehicles(object):

#     class Vehicle1(Fixture):
#         # __model__ = Vehicle
#         id = 1
#         name = u'ff'
#         category = VehicleCategories.VehicleCategory_car

#     class Vehicle2(Fixture):
#         # __model__ = Vehicle
#         id = 2
#         name = u'gg'
#         category = VehicleCategories.VehicleCategory_car


# class Users(object):

#     class RobCowie(Fixture):
#         # __model__ = User
#         id = 1
#         name = u'Rob Cowie'
#         vehicle = Vehicles.Vehicle1

#     class RichTea(Fixture):
#         # __model__ = User
#         id = 2
#         name = u'Rich Taylor'
#         vehicle = Vehicles.Vehicle2
