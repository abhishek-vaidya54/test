import datetime
from datetime import date
import copy
import operator
import json
import logging
import sqlalchemy as sa
from sqlalchemy.sql import text
from sqlalchemy.orm import joinedload, subqueryload
from sqlalchemy.orm.exc import NoResultFound, UnmappedInstanceError
from sqlalchemy.exc import OperationalError, DataError, IntegrityError, SQLAlchemyError, DBAPIError

from pipeline.config import Config
from pipeline import db
from pipeline.db.processed_file import COMPLETE
from pipeline.db.questions.external_dashboard_queries.utils import (
    get_date_range,
    apply_warehouse_filter,
    _set_athletes_count,
    apply_warehouse_filter_athletes
)


from pipeline import date_time_utils as dtu
from pipeline.db import Activity
from flask import abort
import boto3
import pyexcel as pe
import sys
import re
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
class DateInvalidError():
    """Exception to raise on invalid dates back in 90 years """
    pass
class GenderInvalidError():
    """Exception to raise on invalid gender """
    pass
class PriorInjuriesInvalidError():
    """Exception to raise on invalid Prior Injuries """
    pass

"""
# Intiate the process to check validation errors in file
"""
db_engine = create_engine(Config.DB_URL)
session_factory = sessionmaker(bind=db_engine)
#session = scoped_session(session_factory)

s1 = session_factory()
s2 = session_factory()
#s1.rollback()
def init_validation_csv(request):
    if 'file' in request.files:
        logging.warning(request.files)
        filename = request.files['file'].filename
        if filename:
            extension = filename.split(".")[1]
            content = request.files['file'].getvalue()
            if sys.version_info[0] > 2:
                # in order to support python have to decode bytes to str
                content = content.decode('utf-8')
            records = pe.iget_records(file_type=extension, file_content=content)
            errors = []
            row_number = 2
            total_records = 0
            for row in records:
                logging.info(total_records)
                total_records += 1
                error = validate_record(row, row_number)
                if error:
                    errors += error
                row_number += 1
            if errors:
                status = False
            else:
                status = True
            return status, errors, total_records
"""
# Check each column in csv for empty 
"""
def validate_record(row, row_number, import_record):
    error = 0
    modify_row_columns(row)
    if 'first_name' in row and row['first_name'] == "":
        msg = "First name is empty at row {}".format(row_number)
        insert_error(row_number, import_record, msg)
        error += 1

    if 'last_name' in row and row['last_name'] == "":
        msg = "Last name is empty at row {}".format(row_number)
        insert_error(row_number, import_record, msg)
        error += 1
    if 'external_id' in row and row['external_id'] == "":
        msg = "Customer ID is empty at row {}".format(row_number)
        insert_error(row_number, import_record, msg)
        error += 1
    if 'gender' in row and row['gender'] == "":
        msg = "Gender is empty at row {}".format(row_number)
        insert_error(row_number, import_record, msg)
        error += 1
    if 'prior_back_injuries' in row and row['prior_back_injuries'] == "":
        msg = "Known Prior Back Injuries is empty at row {}".format(row_number)
        insert_error(row_number, import_record, msg)
        error += 1
    if 'job_function' in row and row['job_function'] == "":
        msg = "Job Function is empty at row {}".format(row_number)
        insert_error(row_number, import_record, msg)
        error += 1
    if 'shift' in row and row['shift'] == "":
        msg = "Shift is empty at row {}".format(row_number)
        insert_error(row_number, import_record, msg)
        error += 1
    return error

def valid_columns(content,import_record):
    if sys.version_info[0] > 2:
        content = content.decode('utf-8')
    records = pe.iget_records(file_type='csv', file_content=content)

    keys = sorted(['*First Name' , '*Last Name' , '*Customer ID' ,'*Gender (M/F/Other)',
            'Weight (lbs)', 'Height (in)' , 'Hire Date (mm/dd/yyyy)' ,
            '*Known Prior Back Injuries (Y/N/Do Not Specifiy)' , '*Job Function' , '*Shift'])
    logging.info(keys)
    row = records.next()
    rowKeys = sorted(list(set(list(row.keys()))))
    i = 0
    logging.info(sorted(rowKeys))
    for key in rowKeys:
        logging.info(key)
        try:
            if key not in keys:
                logging.info("true")
                msg = "Head column name should be {} not {}".format(keys[i], key)
                insert_error(1, import_record, msg)
        except (ValueError,IndexError):
            msg = "There are extra columns found in header row of csv remove them please "
            insert_error(1, import_record, msg)
        i += 1
"""
# check each header colmn of csv file 
# replace to column names in data base
"""
def modify_row_columns(row):
    for key, value in row.items():
        if '*First Name' in key:
            new_key = 'first_name'
            changekey(row,new_key,key,value)
        if '*Last Name' in key:
            new_key = 'last_name'
            changekey(row,new_key,key,value)
        if '*Customer ID' in key:
            new_key = 'external_id'
            changekey(row,new_key,key,value)
        if '*Gender (M/F/Other)' in key:
            new_key = 'gender'
            changekey(row,new_key,key,value)
        if 'Weight (lbs)' in key:
            new_key = 'weight'
            changekey(row,new_key,key,value)
        if 'Height (in)' in key:
            new_key = 'height'
            changekey(row,new_key,key,value)
        if '*Known Prior Back Injuries (Y/N/Do Not Specifiy)' in key:
            new_key = 'prior_back_injuries'
            changekey(row,new_key,key,value)
        if 'Hire Date (mm/dd/yyyy)' in key:
            new_key = 'hire_date'
            changekey(row,new_key,key,value)
        if '*Job Function' in key:
            new_key = 'job_function'
            changekey(row,new_key,key,value)
        if '*Shift' in key:
            new_key = 'shift'
            changekey(row,new_key,key,value)
            
"""
# Change the key to new key
"""
def changekey(row,newkey,key,value):
    if key != newkey:
        row[newkey] = value
        del row[key]

"""
# start bulk upload process 
# read file from s3
# make it sheet 
# read that sheet with pyexcel lib get_records method
"""
def start_process(location, file_name, s3_bucket, client, warehouse, id, user_id):
    session = boto3.Session(
            aws_access_key_id='AKIAJCOTAHRIMHSF6GYA',
            aws_secret_access_key='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',
            region_name='us-east-1',
    )
    s3 = session.resource('s3')
    fileobj = s3.Object(s3_bucket, file_name).get()['Body']
    content = fileobj.read().rstrip()
    sheet = pe.Sheet()
    sheet.csv = content
    records = pe.get_records(file_type='csv', file_content=content)
    valid_columns(content, id)
    total_records = 0
    inserted_records = 0
    errors = 0
    row_number = 2
    for row in records:
        total_records += 1
        status = insert_process(row, row_number, client, warehouse,id, user_id)
        if status:
            inserted_records += 1
        else:
            errors += 1
        row_number += 1
    if errors > 0:
        s1.rollback()
        s2.commit()
        s2.close()
        s1.close()
        save_activity_import(user_id, client, 'process csv error', id, 'ERRORS')
        return errors, total_records, inserted_records
    else:
        try:
            s1.commit()
            s1.close()
            save_activity_import(user_id, client, 'process csv success', id, 'CREATED')
            return errors, total_records, inserted_records
        except (Exception,KeyError) as exp:
            #logging.info(exp)
            msg = "Insertion failed due to Error:{}".format(exp)
            insert_error(row_number, id, msg)
        except IntegrityError as e: 
            logging.info(e)
            insert_error(row_number, id, e.message)
        
       

def is_shift(row, row_number, import_record, warehouse):
    if 'shift' in row and row['shift'] != "":
        query1 = db.db.session.query(db.Shifts).filter(db.Shifts.name == row['shift'])
        query1 = apply_warehouse_filter(query1, warehouse, column=db.Shifts.warehouse_id)
        shift = query1.first()
        if not shift:
            msg = "Shift does not exist in this warehouse"
            insert_error(row_number, import_record, msg)
        return shift

def is_job_function(row, row_number, import_record, warehouse):
    if 'job_function' in row and row['job_function'] != "":
        query2 = db.db.session.query(db.JobFunction).filter(db.JobFunction.name == row['job_function'])
        query2 = apply_warehouse_filter(query2, warehouse, column=db.JobFunction.warehouse_id)
        job_function = query2.first()
        if not job_function:
            msg = "Job Function does not exist in this warehouse"
            insert_error(row_number, import_record, msg)
        return job_function

"""
# Kick off insert process for add athlete
"""
def insert_process(row, row_number, client, warehouse, import_record, user_id):
    status = False
    modify_row_columns(row)
    
    shift = is_shift(row, row_number, import_record, warehouse)
    job_function = is_job_function(row, row_number, import_record, warehouse)
    if 'hire_date' in row and row['hire_date'] is not None:
        row['hire_date'] = dtu.strp_date(row['hire_date'])
    valid = db_validation(row, row_number, import_record)
    if shift and job_function and valid:
        try:
            athlete = db.IndustrialAthlete(
                first_name = row['first_name'], 
                last_name = row['last_name'],
                name = row['first_name'] + ' ' + row['last_name'],
                gender = row['gender'].lower(),
                height = row['height'],
                weight = row['weight'],
                hire_date = row["hire_date"],
                external_id = row['external_id'],
                job_function_id = job_function.id, 
                shift_id = shift.id,
                prior_back_injuries = row['prior_back_injuries'].lower(),
                warehouse_id = warehouse,
                client_id = client,
                import_record_id = import_record 
                )
            s1.add(athlete)
            status = True
        except (Exception,KeyError) as exp:
            #logging.info(exp)
            msg = "Insertion failed column {} does not exist in the records".format(exp.message)
            insert_error(row_number, import_record, msg)
        except SQLAlchemyError as e: 
            logging.info(e)
            insert_error(row_number, import_record, e.message)
    
        except OperationalError as e:  
            logging.info(e)
            insert_error(row_number, import_record, e.message)
    
        except DataError as e:  
            logging.info(e)
            insert_error(row_number, import_record, e.message) 
    
        except IntegrityError as e: 
            logging.info(e)
            insert_error(row_number, import_record, e.message)
        
        except DBAPIError as e:
            logging.info(e)
            insert_error(row_number, import_record, e.message)
        
    return status

"""
# Insert errors to import_error table
"""
def insert_error(row_number, import_record, msg):
    importerror = ImportErrors(
        row_number = row_number, 
        import_record_id = import_record,
        error_info = msg)
    s2.add(importerror)
    
    #db.db.session.flush()

def db_validation(row, row_number, import_record):
    errors = 0
    error = validate_record(row, row_number, import_record)
    if 'first_name' in row and row['first_name'] !="" and re.findall('[^A-Za-z ]',str(row['first_name'])):
        logging.info(str(row['first_name']))
        msg = "First Name should be a Text/String "
        insert_error(row_number, import_record, msg)
        errors += 1
    
    if 'last_name' in row and row['last_name'] !="" and re.findall('[^A-Za-z ]',str(row['last_name'])):
        logging.info(str(row['last_name']))
        msg = "Last Name should be a Text/String "
        insert_error(row_number, import_record, msg)
        errors += 1
    
    if 'hire_date' in row and row['hire_date'] !="" and not validate_date(row['hire_date']):
        msg = "Hire Date should not exceed 90 years backwards from the current day"
        insert_error(row_number, import_record, msg)
        errors += 1
    
    if 'hire_date' not in row or 'gender' not in row or 'prior_back_injuries' not in row or\
         'height' not in row or 'weight' not in row or 'first_name' not in row or 'last_name' not in row or 'external_id' not in row :
        #msg = "Head Column Hire Date not available in sheet"
        #insert_error(row_number, import_record, msg)
        errors += 1
    
    if 'gender' in row and not validate_gender(row['gender']):
        msg = "Gender value should be F/M/O "
        insert_error(row_number, import_record, msg)
        errors += 1
    
    if 'prior_back_injuries' in row and  not validate_pi(row['prior_back_injuries']):
        msg = "Known Prior Back Injuries value should be Y/N/Do not specify"
        insert_error(row_number, import_record, msg)
        errors += 1
    
    if 'height' in row and row['height'] !="" and not isinstance(row['height'],int):
        msg = "Height should be an integer not Text/String"
        insert_error(row_number, import_record, msg)
    
    if 'weight' in row and row['weight'] !="" and not isinstance(row['weight'],int):
        msg = "Weight should be an integer not Text/String"
        insert_error(row_number, import_record, msg)
        errors += 1
    errors += error
    if errors == 0:
        return True
    else:
        return False
    

"""
# validate date if it is not exceding 90 years in back
"""
def validate_date(hire_date):
    delta_days = (date.today() - hire_date.date()).days/365
    if delta_days > 90:
        return False 
    else:
        return True

def validate_gender(gender):
    glist = ["F","M","O","f","m","o"]
    if gender in glist:
        return True
    else:
        return False

def validate_pi(pi):
    glist = ["Y","N","Do Not Specify","y","n","do not specify"]
    if pi in glist:
        return True
    else:
        return False

def get_errors(id):
    error_session = session_factory()
    import_errors = []
    query = error_session.query(ImportErrors)
    query = query.filter(ImportErrors.import_record_id== id)
    error_session.close()
    data = [row for row in query]
    for row in data:
        import_error = {
            'row_num':row.row_number,
            'error_info':row.error_info
        }
        import_errors.append(import_error)
    return import_errors

def save_activity_import(user_id, client_id, entity_type, entity_id, action):
    activity_session = session_factory()
    activity = Activity(
        user_id=user_id,
        client_id=client_id,
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        #before_state=before_state,
        #after_state=after_state,
        db_created_at=datetime.datetime.now(),
        db_modified_at=datetime.datetime.now()
        )
    activity_session.add(activity)
    activity_session.commit()
    activity_session.close()