def get_job_function(connection, job_function_id, warehouse_id):
    """
    Helper method to retrieve the JobFunction object from the database
    Input:
        job_function_id: Id of the job function
        warehouse_id: Id of the warehouse
    Output:
        job_function: The JobFunction object retrieved from the database
    """
    job_function = connection.execute(
        "SELECT * FROM job_function WHERE id={} AND warehouse_id={}".format(
            job_function_id, warehouse_id
        )
    ).fetchone()
    return job_function


def get_job_function_by_name(connection, name, warehouse_id):
    """
    Get the JobFunction via name
    """
    job_function = connection.execute(
        f'SELECT * FROM job_function WHERE name="{name}" and warehouse_id={warehouse_id}'
    ).fetchone()

    return job_function
