# database-models

To build docker container 
`./docker/start_database_server`


To generate a new migration script
`alembic revision -m 'name'`

To run the migration script (run in dev branch for staging db before running in master branch for prod db)
`alembic upgrade head`

To undo the migration by one version
`alembic downgrade -1`
