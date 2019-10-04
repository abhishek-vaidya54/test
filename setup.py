from setuptools import setup, find_packages

setup(
    name='sat_orm',
    version='0.0.7',
    packages= find_packages('src'),
    package_dir={'':'src'},
    install_requires=[
        'sqlalchemy','pymysql','pytest','factory-boy', 'smalluuid'
    ]
)

