import os


def create_test_pipeline():
    """Function to create test_pipeline database for test cases using pipeline schema
    Output: Raise Error if Database is not created
            else return True
    """
    is_created = True
    try:
        # pipeline database backup
        os.system(
            "sudo docker exec database_container /usr/bin/mysqldump -u root --password=password --no-data pipeline > backup.sql"
        )
        # Add creation line of test database at the beginning of backup script
        file_backup = open("backup.sql", "r+")
        lines = file_backup.readlines()
        file_backup.seek(0)
        file_backup.write("DROP SCHEMA IF EXISTS test_pipeline;")
        file_backup.write("CREATE DATABASE test_pipeline;Use test_pipeline;")
        for line in lines:
            file_backup.write(line)
        file_backup.close()
        # Restore pipeline database structure into test_pipeline database
        check_created = os.system(
            'sudo docker exec -it database_container mysql -u root -ppassword  -e "$(cat backup.sql)"'
        )
        if check_created == 256:
            is_created = False
        os.remove("backup.sql")
    except Exception as e:
        # print(e)
        is_created = False
        return is_created, e
    return is_created, None
    # return True, None


def drop_test_pipeline(test_session):
    """Function to delete test_pipeline database
    Output: If Database is not deleted return False
            else return True
    """
    try:
        # Delete test_pipeline database
        test_session.execute("DROP DATABASE test_pipeline;")
    except:
        return False
    return True


# create_test_pipeline()