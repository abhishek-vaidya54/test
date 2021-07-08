from setuptools import setup, find_packages

setup(
    name="sat_orm",
    version="0.3.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "sqlalchemy==1.4.20",
        "pymysql==1.0.2",
        "pytest==6.2.4",
        "factory-boy==3.2.0",
        "smalluuid==1.1.0",
    ],
)
