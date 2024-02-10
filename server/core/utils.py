from uuid import UUID

from rest_framework.exceptions import ValidationError
from django.conf import settings

import io
import csv

def is_valid_uuid(uuid_to_test, version=4):
    '''
    checks if uuid is valid
    '''
    try:
        if uuid_to_test is None:
            raise ValueError
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test

def valid_uuid_or_error(uuid_to_test, version=4, error_message:str=None):
    '''
    confirms a valid uuid or raises a DRF validation error
    '''
    if not is_valid_uuid(uuid_to_test, version):
        if error_message is None:
            error_message = "invalid uuid"
        raise ValidationError(error_message)
    
@staticmethod
def csv_file_to_list(request, name:str, slice_func:int, slicing_error_msg:str=None, hints:str=None):
    '''
    return a list of the lines from a CSV file in a request
    '''
    upload_file = request.FILES.get(name)
    if upload_file is None:
        raise ValidationError(
            {"detail":"file for '%s' was not provided" % name}
            )
    if upload_file.content_type != "text/csv":
        raise ValidationError(
            {"detail":"expected a 'text/csv' as content type, not '%s'" % upload_file.content_type}
            )
    io_string = io.StringIO(upload_file.read().decode())
    read = csv.reader(io_string)
    try:
        return [i[slice_func] for i in read]
    except IndexError:
        response = {}
        if slicing_error_msg is None:
            slicing_error_msg = (
                "file '%s' format was not able to be parsed. "
                "Ensure that the file format follows the protocol the API endpoint is requesting"
                ) % name
        response["detail"] = slicing_error_msg
        if hints:
            response["hints"] = hints
        raise ValidationError(response)
    
def get_data_from_csv(request):
    return csv_file_to_list(
        request,
        name=settings.DATA_CSV_LOOKUP, 
        slice_func=slice(4),
        hints="each line requires n items of 'subject_codes'"
    )
    
def get_options_from_csv(request):
    return csv_file_to_list(
        request,
        name=settings.OPTIONS_CSV_LOOKUP, 
        slice_func=1,
        hints="each line requires two items 'subject_name','subject_code'"
    )
    
from django.core import exceptions
import json
    
def load_form_data(request) -> dict:
    payload = request.data.get("payload")
    if payload is None:
        raise exceptions.ValidationError({"detail":"payload required as form data"})
    return json.loads(payload)
