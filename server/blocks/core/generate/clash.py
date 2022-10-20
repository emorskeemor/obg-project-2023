# methods for matching and subject clashing

from itertools import combinations
from typing import Any, Dict, Iterable, List, Tuple

# clash methods

def clash_count(subjects:Iterable, data:Dict[Any,List]):
    '''
    returns a count of the number of times an arbitrary number of subjects
    exist in student's choices. e.g. checking Fr, Ge will return a count where
    Fr and Ge BOTH exist in a student's choices
    '''
    count = 0
    for student_options in data.values():
        matched = sum([1 for subj in set(subjects) if subj in student_options])
        if matched == len(subjects):
            count += 1
    return count
        

def clash_matrix(option_codes:List):
    '''
    generates a clash matrix
    '''
    clashes = list()
    for comparission in combinations(option_codes, 2):
        # to remove duplicates, create a set to ensure uniqueness
        if len(set(comparission)) == 2:
            clashes.append(tuple(comparission))
    return clashes

def evalute_clashes(clashes:set, data:Dict[Any, List]):
    '''
    returns a dictionary of clashes and their counts
    '''
    # essentially, we go through each clash from a set of clashes
    # and check each students option's to see how often it clashes
    return {clash:clash_count(clash, data) for clash in clashes}

def order_clashes(clashes:Dict[Tuple, int], reverse=True):
    '''
    order a dictionary of clashes by the number of clashes
    '''
    return {clashes:value for clashes, value in sorted(clashes.items(), key=lambda x:x[1], reverse=reverse)}

def filter_clashes(clashes:Dict[Tuple, int], conditional_func:Any=None):
    '''
    return clashes filtered by a given conditional function. E.g.
    lambda x:x[1] > 1 returns all clashes greater than 1
    '''
    return dict(filter(conditional_func, clashes.items()))

# These methods are deprecated and can be too inefficent to run

def subject_block_clashes(subject_code:str, block:List, data:Dict[Any,List]):
    '''
    [DEPRECATED]
    displays the number of clashes occurs between a subject provided and
    for each subject within a block. Returns the maximum clash count
    '''
    return sum([clash_count((subject_code, subject), data) for subject in block])

def total_block_clashes(subject_code:str, blocks:List[List], data):
    '''
    [DEPRECATED]
    returns a list of the clashes of a subject against a each block. 
    This has an overall time complexity of O(n^4) which is inefficient. It is recommened
    to cache clashes so they can be looked up in a dictionary before calculating the 
    clashes
    '''
    clash_counts = [subject_block_clashes(subject_code, block, data) for block in blocks]
    return clash_counts

# more efficient ways of calculating clashes

def cached_subject_block_clashes(subject_code:str, block:List, data:Dict[Any,List], cache:Dict):
    '''
    similar to 'subject_block_clashes' but caches using a given dictionary and returns the clash
    count and a dictionary that has not yet been cahed
    '''
    clashes = 0
    updated_cache = {}
    for subject in block:
        # sort the clash as, when we are using a clash matrix, the clashes will be ordered
        # by alphabetical order. We need to do this to cache properly and find the correct
        # cached value if it exists
        clash = tuple(sorted((subject, subject_code)))
        cached = cache.get(clash, None)
        if cached is None:
            count = clash_count(clash, data)
            updated_cache.update({clash:count})
            clashes += count
        else:
            clashes += cached
    return clashes, updated_cache

def cached_total_block_count(subject_code:str, blocks:List[List], data:Dict[Any,List], cache:Dict) -> Tuple[List[int], Dict[Tuple[str,str], int]]:
    '''
    cached version of 'total_block_clashes' which looks up the clash in a cache dict before
    calculating the clash. Returns a list of clash counts and an an updated version of the cache
    with clashes that were not yet cached
    '''
    # clash_counts = [cached_subject_block_clashes(subject_code, block, data, cache) for block in blocks]
    # return clash_counts
    clash_counts = []
    for block in blocks:
        count, updated_cache = cached_subject_block_clashes(subject_code, block, data, cache)
        clash_counts.append(count)
        cache.update(updated_cache)
    return clash_counts, cache


# matching methods

def match_subjects(subjects, data:Dict[Any,List]):
    '''
    very similar to 'clash_count' but returns the matches students
    instead
    '''
    matched_subjects = dict()
    for key, student_options in data.items():
        matched = sum([1 for subj in subjects if subj in student_options])
        if matched == len(subjects):
            matched_subjects[key] = student_options
    return matched_subjects
