import operator
from typing import Any, Dict, Iterable, List, Set, Tuple

from blocks.core.exceptions import SavePointRequired, WatchGuardTriggered
from blocks.core.generate.clash import filter_clashes
from blocks.core.generate.population import PopulatorMixin
from blocks.core.pregenerate.statistics import filter_grouped_by


class BaseProcess(PopulatorMixin):
    '''
    base class for all processes. Contains methods for block population and requires
    parameters referenced from the SaveNode class that will be manipulated
    '''
    def __init__(self, blocks, data, cache, required, used, grouped, together, enabled=True) -> None:
        super().__init__()
        # these attributes must match those of the populator mixin
        self.blocks: List[List[str]] = blocks
        self.DATA: Dict[Any, List] = data
        self.cache:Dict = cache
        self.classes_per_subject:Dict = required
        self.used:Set[str] = used
        self.enable_sp:bool = enabled
        self.together:Dict[str, Tuple[Tuple, int]] = together
        self.grouped:Dict = grouped

    def run_process(self):
        '''
        code that manipulates the blocks
        '''
        raise NotImplementedError("state process not implemented")

    def __call__(self) -> Any:

        self.run_process()
        

class Priority(BaseProcess):

    def run_process(self):
        # deal with the priorities. These are subjects that only have 1 class
        # and have high clash count
        single_subjects = filter_grouped_by(self.grouped, 1)
        matrix = self.get_matrix(single_subjects)
        priority = filter_clashes(matrix, lambda x:x[1] >= 2)
        for clash in priority.keys():
            first, second = clash
            self.populate_lowest_block(first, 1)
            self.populate_lowest_block(second,1)

class RemainingSingles(BaseProcess):
    
    def run_process(self):
        # deal with the remaining single subjects
        single_subjects = filter_grouped_by(self.grouped, 1)
        # raise the priority shift only if it hasnt already been completed        
        rest = set(self.used).symmetric_difference(single_subjects)
        
        for subject in rest:
            self.populate_lowest_block(subject, 1)
    
class MainProcess(BaseProcess):

    def __build_classes(self, subject_codes:Iterable, useage:int):
        for subject in subject_codes:
            self.populate_lowest_block(subject, useage)

    def run_process(self):
        # the main process of populating subjects that require more than 1 class
        # and less than number of blocks

        for use in range(len(self.blocks)):
            opts = filter_grouped_by(self.grouped, use)
            self.__build_classes(opts.keys(), use)

class Negligible(BaseProcess):
    
    def run_process(self):
        # this deals with the subjects that match the same number of blocks
        # or greater. We might as well populate all of the blocks with these subjects
        # as they are negligible
        overloaded = filter_grouped_by(self.grouped,len(self.blocks),
            operation=operator.ge
            )
        for subject in overloaded:
            self.populate_all_blocks(subject)
        

STATE_PROCESS = [Priority, RemainingSingles, MainProcess, Negligible]