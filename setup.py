from setuptools import setup

setup( name='sir_model',
       packages=['sir_model'],
       entry_points={
           'console_scripts': ['sir_model=sir_model.main:main'] } )
