from typing import Any, Dict, List, Tuple

from blocks.core.exceptions import SubjectNotFound


def subject_counts(data:Dict[str, List], option_codes:List[str]):
    '''
    gets the counts of each subject from a dataset
    '''
    counts = dict.fromkeys(option_codes, 0)

    for student_opts in data.values():
        for option in student_opts:
            current_value = counts.get(option, None)  
            if current_value is None:
                raise SubjectNotFound(
                    "subject '%s' was not found in the available options" % option
                    )
            counts[option] = current_value + 1
    return counts

def subject_block_count(option_codes:List[str], blocks:List[List]):
    '''
    count the occurances of options in a given set of blocks
    '''
    counts = dict.fromkeys(option_codes, 0)

    for option in option_codes:
        value = counts.get(option, None)
        occurances = 0
        for block in blocks:
            if block is None:
                continue
            if option in block:
                occurances += 1
        counts[option] = value + occurances
    return counts

def group_by_class(counts:Dict[str, int], class_size:int):
    '''
    returns a dict of {subject_code:(popularity_count:classes_for_subject)}
    for each of the subject counts
    '''
    return {subj_code:(count, int(count)//class_size+1) for subj_code,count in counts.items()}


import operator


def filter_grouped_by(counts:Dict[str, Tuple[int,int]], value:int, operation:Any=operator.eq, by="classes"):
    '''
    order the grouped counts.
    '''
    assert by == "classes" or by == "subjects", "'by' must be either 'classes' or 'subjects'"
    by = 1 if by == "classes" else 0
    return dict(filter(lambda i:operation(i[1][by], value), counts.items()))