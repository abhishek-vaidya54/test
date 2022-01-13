"""
NAME: Dockv5 Events Log ORM

DESCRIPTION:
            The dockv5_eventslog_orm package is a presentation of the orms for the dockv5
            schema. As the table schema is deliccate and can affect other
            files when changes, the goal of the orm is to match with the
            schema at all times, meaning that we can now represent the 
            dockv5 schema as lines of code.
            
            +-------------------+
            | DockEvents Tables |
            +-------------------+
            | appcrash_log      |
            | data_events       |
            | engagement_stats  |
            | keepalive_events  |
            | monthly_safety    |
            | raw_event_log     |
            | sensor_events     |
            | survey_events     |
            +-------------------+

            **** Edit This File If tables are added or removed ****
"""
