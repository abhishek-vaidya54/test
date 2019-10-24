SAT ORM
===
For easier database maintenance

# setup
copy .envrc.sample in this directory to .envrc and set the vault token
(vault token should be created from database vault policy)

To build docker container to run mysql locally and test changes locally
`./docker/start_database_server`

# Introduction
Object Relational Mapper or (ORM) are used to interact with a database using the programming
language that they are written in. Here at SAT our ORMs are designed using the python programming 
language with the help of [sqlalchemy](https://www.sqlalchemy.org/), a Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL. 

To start using this package in your SAT project simply pip install the package. Before you try and install the
package, make sure that your machine has a github ssh key, to give it the possibility to access the repository.
```s

python3 -m pip install -e git+ssh://git@github.com/strongarm-tech/database_models.git@master#egg=sat_orm
```
This will install the sat_orm package onto your machine. Once it is completed run pytest to make sure that 
the package installed correctly:

```s
python3 -m pytest --pyargs sat_orm
```
This will run pytest and help you setup your machine so that it is compatible for the package. Once you have setup your machine and all the test pass, you are ready to use the ORM's.

# Getting Familiar with SAT ORM
SAT ORM was designed to be simple to use and integrate into your current projects. Once you have it installed on your machine, the first step is to import the orm class that you want to add your project.

## From Import to Pro

```python
from sat_orm.dockv5 import Config, DockPhase
#   from package_name.schemaname import table1, table2, session
```
This is the syntaxt for importing database tables to your python script. You first call the sat_orm, then you link it to the database schema, from there you import the proper table. The table is always initialized with the Columns, So all you have to do to create an insert is:

```python
# Initialize the row you would like to create 
config = Config(dock_id='E3D5F6D332A1A4',deployment_stage='dev'...)

# Then added to your session
session.add(config)

# Then Commit your new row to the database
session.commit()
```

importing `session` is crucial as well so that the database know where the table is located and can add the rows properly. The session is located in the `*_base.py` file. All Connection to the database are located in that file as well. Once you are done and you have commited your changes, please me sure to close the session by doing: `session.close()`

Once you get comfortable with the architecture, its time for you to move on to the fun stuff. Next the goal is to fo a query search. Query search are simple, because it is base off of [sqlalchemy](https://www.sqlalchemy.org/) feel free to go to there website to learn more about querying with SQLAlchemy. However here are some common examples:

```python
from sat_orm.dockv5 import Config, session

# Returns the first row in config table where dock_id = dock_id
config = session.query(Config).filter_by(dock_id='E3D5F6D332A1A4').first()

# if you was it as a dictionary
config_as_dict = config.as_dict()

# from there you can access the data in two different ways:
print(config.dock_id)
# or
print(config_as_dict['dock_id'])
```

The simplicity of sqlalchemy makes it easy to work with our databases. Now that we are familiar with the ORM classes, lets move on to contributing to sat_orm.

# Running Migrations
There are two ways to run migrations currently, locally and Online. Locally lets you update the database running on your local machine. The first thing you want to do is create a migration script. Here at SAT we use [alemic](https://alembic.sqlalchemy.org/en/latest/) to create migration scripts. By doing `alembic revision -m 'adding_new_column_to_tablename'` will generate a migration script in `alembic/versions`. To run this command, make sure you are in the right folder. To run migrations for dockv5, make sure you are in the dockv5 directory located at the root of the database_models folder. It is the same for the other schemas. Once you've create your migration script, make sure you also change the `env.py` file if you are trying to run it locally. Checkout the [Editing Database](https://github.com/strongarm-tech/database_models/wiki/Editing-Database) wiki page for more information. 

Once you are ready to make your migration run `alembic upgrade head`, this will update your database according to your changes. If you realized you need to downgrade it, simply run `alembic downgrade -1`.

# Contribution
As we grow changes to the ORM's will be continuous, the good thing is that they help keep a single source of truth for the database. Being able to contribute to the growth of this product properly is essential to the success of sat_orm. We will first start with Why to contribute, then we will give a tutorial on how to contribute and lastly what to look out for when contributing.

## Why Contribute
The ORM's are not objects that will stay constent. As our needs changes the ORM's capability will change with them as well. While implementing ORMs you will realize that all the functionalities are not included, meaning that you will find yourself writing out a lot of queries that will be repeated throughout your code. Once that start happening, then it is probably better if you update the ORM scripts to include a new method that does the work.

Impletmenting methods that uses the ORMs are setup a little different. To import a method you import the `_orm.py` file instead of the class.

```python
# from the sat_orm folder open the dockv5_orm folder and then import the config module.
from sat_orm.dockv5_orm import config # config is a module
from sat_orm.dockv5 import session # session is a sqlalchemy class

# insert_or_update is a method inside the config module
config.insert_or_update(session,data)
```

Adding all of the config methods outside of the class makes it easier to access those methods without having to initialize the class. You can do `config.Config(dock_id=...)` but you might run into relation issues. Once you understand why it is important to contribute. The next section will give you an idea as to how to contribute successfully to the sat_orm package.

## How to Contribute
To contribute to sat_orm package there is a guide to help everyone know how the package is doing and what is being updated. 

| Name | Description |
|:----:|:-----------:|
| Create Issue | Make sure to add the issue that you would like to fix in your jira board. This makes it easy to track what you are changing and what has been changed |
| Create New Branch | Create a new branch off of staging, with the name of the issue and your last name added at the ebd. ei: adding_insert_or_update_turnier. The first 4 words is the name of the issue, the last word is your lastname or name of contributor. |
| Write Primilinary Test | Write test cases for what you expect your changed to do. It does not need to include all of the test cases, However a minimum amount to let someone else pick it up and understand what you were trying to do. |
| Create Method | Write out your function, and run it against the test to see if you are on the write track |
| Improve test | Improve your test cases. Make sure to document them well, so that new users can easily use your new code |
| Add Documentation | Add documentation for the new method that was added. Important so that others do not create the same method that already exist |
| Make a Pull Request | Create a pull request to staging so that another team member can review your changes. Teammate will follow the guide to make sure that everything is up to standard. They will also run the test locally to make sure that all of them pass. They will also check to code coverage to see if the coverage is up to our standards, before accepting the Pull Request |

### Create Issue
Creating issues in jira is important so that the dev team knows exactly what you are working on, and what you are planning to add to the sat_orm package. It will also let others give their input before you start working on a new feauture for the package. This will also help you track what needs to be done for the package is being upgrade as needed.

### Create New Branch
Creating a new branch is easy, it is as simple as following our project flow. Make sure to branch off of staging, as every feature merges to staging first before it is pushed to production. If you are not used to our git flow, [here]() is a link to a diagram. The naming convention for new feature for the sat_orm package is important, as others get to see which features are being added. Adding your last name at the end of the new branch name is crucial to let teammates know who the branch is owned by.

### Writting Primilinary Test
Writing primilinary test cases is crucial to development of your new feautures, it will help you know what to focus on. If you are adding a new feauture there is obviously a reason for that. It might be to return back a specific query or do some calculations for you, whatever it is you already know what the output should be. What the output will be is there first thing you will assert. The following is an example on how to implement a primilinary test on a random function.
```python
@pytest.makr.test_orm_method
def test_config_create_method():
    config.create(dock_id=dock_id,...)
    session.commit()
    config_row = session.query(Config).filter_by(dock_id=dock_id).first()
    assert config_row != None
```
From there as you start running the test you will know what to add and make sure that it works. Once you have reached the PASS, you will want to add more test cases to make it robust.

### Create Method
This is straight forward. Start creating your new method until your primilinary test case passes

### Improve Test
Improving Test means that you are adding more test cases to your test module. As you add more cases you make your code more robust and helps others understand what it can and cannot do. Thinking of edge cases and what should happened if they are reached is what to think about when adding more test. Also add how your method will handle them, and check to see if the method handles them correctly.

### Add Documentation
Yes it is cool to write code, However if no one can understand how it works or how to use it, there is no use in what you wrote. Documentation of `sat_orm` is what will make it a successful product. When documenting, think about what you would want someone to tell you if it was your first time using the product. Even if it is easy to use, explain why and how it is easy to use. Pull Request must always include a link to your documentation. Documentation should be added in the [database models wiki](https://github.com/strongarm-tech/database_models/wiki), there will be a section on how to add and update documentation in there.

### Make Pull Request
Once You have added your issue to Jira, created your new branch, created your primilinary test, coded, improved your test and code, and documented, you are now ready to submit your PR. Submiting a PR is very simple just make sure that you are asking to merge to staging. A teammate will take over, check to see if you followed the procedures, well documented your changes, downloard the package and run the packaged test. Finally check to see the code coverage. Once all of those check out, they will merge your changes to staging.

## Conclusion
Adding new features to `sat_orm` package is simple, and following these procedures will ensure the best quality of the ORM's and of the package overall.

# database-models
[Database Model Wiki
Page](https://github.com/strongarm-tech/database_models/wiki)

## setup
copy .envrc.sample in this directory to .envrc and set the vault token
(vault token should be created from database vault policy)

To build docker container to run mysql locally and test changes locally
`./docker/start_database_server`