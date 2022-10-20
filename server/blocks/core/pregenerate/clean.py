from typing import Iterable, List


def clean_options(options:List[str], max_opts:int=4):
    '''
    returns a cleaned set of options
    '''
    opts = [opt for opt in options if opt.strip()]
    return opts[:max_opts]

def populate_with_id(data:Iterable):
    '''
    populate an iterable data with a default id.
    Normally use for debugging dummy data and 
    creating useable data from a csv for example
    '''
    standardised = {}
    for n, student_options in enumerate(data):
        standardised[n] = student_options
    return standardised

def filter_options(options:Iterable, ignore:Iterable):
    return set(options).difference(ignore)