import os
import re
import subprocess
from enum import Enum

class Direction(Enum):
    """
        Used to determine if the alembic migration to a specific revision is an 
        upgrade, downgrade, or is unnecessary(up to date).
    """
    UPGRADE = 1
    UP_TO_DATE = 2
    DOWNGRADE = 3

def run(cmd):
    """
        Helper function that takes a bash command cmd, runs it, and cleans up 
        the output
    """
    print('$', cmd)
    cmd_list = cmd.split(' ')
    output = subprocess.run(cmd_list, capture_output=True)
    stdout = str(output.stdout, 'utf8')
    stderr = str(output.stderr, 'utf8')
    print(stdout, end='')
    print(stderr, end='')
    print()
    if output.returncode != 0:
        raise Exception('\n'+stderr)
    return stdout

def load_inputs():
    """
        Read the inputs from environemnt variables set by the GitHub workflow
    """
    INPUT_DATABASE_URI = os.environ.get('INPUT_DATABASE_URI')
    INPUT_REVISION_ID = os.environ.get('INPUT_REVISION_ID')
    return INPUT_DATABASE_URI, INPUT_REVISION_ID

def parse_INPUT_DATABASE_URI_to_get_database_and_subaccount(INPUT_DATABASE_URI):
    """
        From the database URI, determine which subaccount and which database
        we are wish to target
    """
    pattern = re.compile(r'''
        (?P<name>[\w\+]+)://
        (?:
            (?P<username>[^:/]*)
            (?::(?P<password>[^/]*))?
        @)?
        (?:
            (?P<host>[^/:]*)
            (?::(?P<port>[^/]*))?
        )?
        (?:/(?P<database>.*))?
        '''
        , re.X)
    m = pattern.match(INPUT_DATABASE_URI)
    if not m:
        raise Exception('Schema is unspedified; Database URI is invalid')
    components = m.groupdict()
    host = components['host']
    INPUT_DATABASE_URI
    database = components['database']
    if (re.search(r'^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$', host)
        or host == 'localhost'):
        subaccount = 'local'
    else:
        if len(host.split('.')) > 1:
            subaccount = host.split('.')[1]
    return subaccount, database

def find_what_the_current_revision_is(subaccount, database):
    """
        Find the current revision ID is in the subaccount & database targetted
    """
    folder_mappings = {
        'pipeline': 'pipeline',
        'dock': 'dockv5',
        'dockEvents': 'dockv5_eventslog'
    }
    if not database in folder_mappings:
        raise Exception(f'Unknown database "{database}"')
    folder = folder_mappings[database]
    os.chdir(folder)
    stdout = run('alembic current')
    m = re.search(r'(\w{12}).*$', stdout)
    current_revision_id = m.groups()[0] if m else ''
    print(f'{database} database running in {subaccount} subaccount is on revision {current_revision_id}')
    return current_revision_id

def find_out_whether_revision_is_upgrade_or_downgrade(INPUT_REVISION_ID, current_revision_id):
    """
        Parse through the alembic history to determine if the revision we are
        targetting would be an upgrade or downgrade from the current one
    """
    stdout = run('alembic history')
    revision_id_list = []
    for line in stdout.split('\n'):
        m = re.search('.* -> (\w{12}).*', line)
        if m:
            revision_id_list.append(m.groups()[0])
    INPUT_REVISION_ID_index, current_revision_id_index = -1, -1
    for i, revision_id in enumerate(revision_id_list):
        if revision_id == INPUT_REVISION_ID:
            INPUT_REVISION_ID_index = i
        if revision_id == current_revision_id:
            current_revision_id_index = i
        if INPUT_REVISION_ID_index != -1 and current_revision_id_index != -1:
            break
    if INPUT_REVISION_ID_index == -1:
        raise Exception(f'"{INPUT_REVISION_ID}" is not a vaild revision ID')
    if current_revision_id_index == -1:
        raise Exception(f'Current revision ID "{current_revision_id}" not contained in history')
    if INPUT_REVISION_ID_index < current_revision_id_index:
        return Direction.UPGRADE
    if INPUT_REVISION_ID_index == current_revision_id_index:
        return Direction.UP_TO_DATE
    if INPUT_REVISION_ID_index > current_revision_id_index:
        return Direction.DOWNGRADE

def go_in_that_direction_to_that_revision(direction, INPUT_REVISION_ID, database, subaccount):
    """
        Run the actual alembic migration
    """
    if direction is Direction.UPGRADE:
        run(f'alembic upgrade {INPUT_REVISION_ID}')
    elif direction is Direction.DOWNGRADE:
        run(f'alembic downgrade {INPUT_REVISION_ID}')
    else:
        print(f'{database} database running in {subaccount} subaccount is already on revision {INPUT_REVISION_ID}')

def main():
    """
        Main function that drives the program.  Reads the inputs and determines
        the necessary action to take to run the alembic migration
    """
    INPUT_DATABASE_URI, INPUT_REVISION_ID = load_inputs()
    subaccount, database =\
        parse_INPUT_DATABASE_URI_to_get_database_and_subaccount(INPUT_DATABASE_URI)
    current_revision_id = find_what_the_current_revision_is(subaccount, database)
    if INPUT_REVISION_ID == 'head':
        direction = Direction.UPGRADE
    else:
        direction =\
            find_out_whether_revision_is_upgrade_or_downgrade(INPUT_REVISION_ID, current_revision_id)
    go_in_that_direction_to_that_revision(direction, INPUT_REVISION_ID, database, subaccount)

if __name__ == "__main__":
    main()
