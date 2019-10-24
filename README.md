SAT ORM
===
For easier database maintenance

# Introduction
Object Relational Mapper or (ORM) are used to interact with a database using the programming
language that they are written in. Here at SAT our ORMs are designed using the python programming 
language with the help of [sqlalchemy](https://www.sqlalchemy.org/), a Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL. 

To start using this package in your SAT project simply pip install the package. Before you try and install the
package, make sure that your machine has a github ssh key, to give it the possibility to access the repository.
```
python3 -m pip install -e git+ssh://git@github.com/strongarm-tech/database_models.git@master#egg=sat_orm
```
This will install the sat_orm package onto your machine. Once it is completed run pytest to make sure that 
the package installed correctly:
```
python3 -m pytest --pyargs sat_orm
```
This will run pytest and help you setup your machine so that it is compatible for the package. Once you have setup your machine and all the test pass, you are ready to use the ORM's.


# database-models
[Database Model Wiki
Page](https://github.com/strongarm-tech/database_models/wiki)
## setup
copy .envrc.sample in this directory to .envrc and set the vault token
(vault token should be created from database vault policy)

To build docker container to run mysql locally and test changes locally
`./docker/start_database_server`

## using alembic

To generate a new migration script
`alembic revision -m 'name'`

To run the migration script (run in dev branch for staging db before running in master branch for prod db)
`alembic upgrade head`

To undo the migration by one version
`alembic downgrade -1`
