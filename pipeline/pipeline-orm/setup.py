from setuptools import setup, find_packages
from pipeline_orm import __version__

setup(
    name='pipeline_orm',
    version=__version__,
    packages= find_packages('src'),
    package_dir={'':'src'},
    install_requires=[
        'sqlalchemy','factory-boy','pymysql','pytest'
    ]
)

