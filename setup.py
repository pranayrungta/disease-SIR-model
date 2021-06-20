from setuptools import setup

setup( name='sir_model',
       packages=['sir_model'],
       author="Pranay, Kanishka",
       author_email="pranay.rungta@gmail.com",
       install_requires=['numpy', 'pyqt5', 'matplotlib'],
       entry_points={
           'console_scripts': ['sir_model=sir_model.main:main'] } )
