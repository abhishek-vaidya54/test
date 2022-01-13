"""
NAME: Pipeline ORM

DESCRIPTION:
            The pipeline_orm package is a presentation of the orms for the dockv5
            schema. As the table schema is deliccate and can affect other
            files when changes, the goal of the orm is to match with the
            schema at all times, meaning that we can now represent the 
            dockv5 schema as lines of code.
            
            +-----------------------+
            | Pipeline Tables       |
            +-----------------------+
            | binary_bucket_monitor |
            | client                |
            | industrial_athlete    |
            | job_function          |
            | messages_surveys      |
            | metadata              |
            | parser_monitor        |
            | processed_file        |
            | risk                  |
            | rule_condition        |
            | rule                  |
            | settings              |
            | shifts                |
            | warehouse             |
            +-----------------------+

            **** Edit This File If tables are added or removed ****
"""
