# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='fixer',
    version='0.0.1',
    author='Rob Cowie',
    author_email='',
    packages=find_packages(),
    description='SQLAlchemy fixture loader',
    # test_suite='',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'networkx==1.7'
    ]
)
