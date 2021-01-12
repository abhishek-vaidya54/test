import os


def create_test_db(db):

    """Function to create test_db database for test cases using db schema
    Output: Raise Error if Database is not created
            else return True
    """
    is_created = True
    try:
        #  database backup
        os.system(
            "sudo docker exec database_container /usr/bin/mysqldump -u root --password=password --no-data {0} > {0}_backup.sql".format(
                db
            )
        )

        # Add creation line of test database at the beginning of backup script
        file_backup = open("{}_backup.sql".format(db), "r+")
        lines = file_backup.readlines()
        file_backup.seek(0)
        file_backup.write(
            "DROP DATABASE IF EXISTS test_{0};CREATE DATABASE test_{0};Use test_{0};".format(
                db
            )
        )
        for line in lines:
            file_backup.write(line)
        file_backup.close()
        # Restore db database structure into test_db database
        check_created = os.system(
            'sudo docker exec -it database_container mysql -u root -ppassword  -e "$(cat {}_backup.sql)"'.format(
                db
            )
        )
        if check_created == 256:
            is_created = False
        os.remove("{}_backup.sql".format(db))
    except Exception as e:
        is_created = False
        return is_created, e

    return is_created, None
