from uuid import UUID

from rest_framework.exceptions import ValidationError

import io
import csv

def is_valid_uuid(uuid_to_test, version=4):
    
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test

def valid_uuid_or_error(uuid_to_test, version=4, error_message:str=None):
    if not is_valid_uuid(uuid_to_test, version):
        if error_message is None:
            error_message = "invalid uuid"
        raise ValidationError(error_message)
    
@staticmethod
def parse_memory_handler(request, name:str, slice_func:int):
    '''return a list of the lines from a CSV file in a request'''
    upload_file = request.FILES.get(name)
    if upload_file is None:
        raise ValidationError({"error":"file for '%s' not provided" % name})
    if upload_file.content_type != "text/csv":
        raise ValidationError({"error":"csv file required"})
    io_string = io.StringIO(upload_file.read().decode())
    read = csv.reader(io_string)
    return [i[slice_func] for i in read]