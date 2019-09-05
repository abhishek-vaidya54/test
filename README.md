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
