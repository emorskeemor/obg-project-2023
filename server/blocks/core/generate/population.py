from typing import Any, Dict, Iterable, List, Set, Tuple

from blocks.core.exceptions import SavePointRequired, WatchGuardTriggered
from blocks.core.generate.clash import (cached_total_block_count, clash_matrix,
                                        evalute_clashes, order_clashes)


class PopulatorMixin:
    '''
    mixin with methods to populate option blocks
    '''

    matrix = None

    def __init__(self) -> None:
        self.blocks:List[List[str]] = None
        self.classes_per_subject:Dict[str, int] = None
        self.used:Set = None
        self.DATA:Dict[Any,List] = None
        self.cache:Dict[Tuple, int] = None
        self.enable_sp = True
        self.together:Dict[str, Tuple[Tuple,int]] = None

    def insert(self, subject:str, block_num:int):
        '''
        insert a given block with a subject
        '''
        # this method is the only way to insert subjects into an option 
        # block. This provides a core method which can then update certain
        # data structures to keep track of what we have done
        useage = self.classes_per_subject.get(subject, 0)
        block = self.blocks[block_num]
        if subject in block or useage <= 0:
            return False
        
                
        self.classes_per_subject.update({subject:useage-1})
        self.used.add(subject)
        block.append(subject)
                
        return True

    def insert_many(self, subjects:Iterable, block_num:int):
        '''
        insert subjects that are required to be inserted together
        '''
        for subject in subjects:
            if self.insert(subject, block_num) is False:
                return False
        return True

    def populate_block(self, subject, block_num:int):
        '''
        proxy that check if the subject requires a double. If not, then
        just populate the block with the given subject
        '''
        # insert the normal subject first
        if self.insert(subject, block_num) is False:
            return False

        # do we need to insert another subject/s with it?
        if many:= self.together.get(subject):
            extra_opts, max_use = many
            # insert the extra subjects
            self.insert_many(extra_opts, block_num)
            # either remove the subject from the together dict as it is 
            # exausted, or reduce the max use count
            if max_use <= 0:
                self.together.pop(subject)
            else:
                self.together.update({subject:(extra_opts, max_use-1)})
        return True


    def populate_lowest_block(self, subject:str, useage:int):
        '''
        populate blocks with a given subject a given number of times (useage) that have the 
        smallest clash count. If there are multiple options, a 'SavePointRequired' 
        exception is raised with details about the possible options and the subject
        that could not be inserted
        '''
        # repeat useage number of times
        for _ in range(useage):
            # get the subject use count and validate to make sure we dont use it too much
            used = self.classes_per_subject.get(subject, 0)
            
            if used <= 0:
                return None
            # get a total clash count for each block and an updated cache
            block_clashes, updated_cache = cached_total_block_count(subject, self.blocks, self.DATA, self.cache)
            block_clashes = list(enumerate(block_clashes))
            self.cache = updated_cache
            
            inserted = False
            # repeat until the subject has been inserted into the block. The reason why
            # we need to iterate is because the lowest clash block might already have that
            # subject within it.
            while inserted is False:
                # get the block with the smallest clash count
                block_num, clash_count = min(block_clashes, key=lambda x:x[1])
                # this if statement checks to see if there is more than one block with the smallest
                # clash count value. If save points are enabled, it then moves onto the next stage
                if [count[1] for count in block_clashes].count(clash_count) > 1 and self.enable_sp:
                    # the smallest clash count might appear twice, this means there is
                    # two routes we could go down
                    opts = list(filter(lambda x:x[1] == clash_count, block_clashes))
                    # we need to verify that the blocks with equal clashes are not empty as it is useless
                    # to create a savepoint for an empty block.
                    if sum([1 for num,_ in opts if self.blocks[num] == []]) == 0:
                        raise SavePointRequired(options=[opt[0] for opt in opts], subject_code=subject)

                if self.populate_block(subject, block_num) is False:
                    # if we weren't able to populate the given block, remove that
                    # block from the block clashes and move on
                    block_clashes.remove((block_num, clash_count))
                else:
                    inserted = True
        
    def populate_all_blocks(self, subject:str):
        '''
        populate all blocks with a given subject
        '''
        for block_number in range(len(self.blocks)):
            self.populate_block(subject, block_number)

    def get_matrix(self, subject_codes:List[str]):
        '''
        generates a clash matrix for priority subjects
        '''
        # if a matrix already exists, we do not need to generate a 
        # new one
        if self.matrix is not None:
            return self.matrix
        # generate the matrix, evaluate it, update our cache
        # and then order it for sanity
        matrix = clash_matrix(subject_codes)
        evaluated = evalute_clashes(matrix, self.DATA)
        
        self.cache.update(evaluated)
        evaluated = order_clashes(evaluated)
        # store the matrix in the populator mixin instead of save node
        # so it can be access by the state classes
        self.matrix = PopulatorMixin.matrix
        PopulatorMixin.matrix = evaluated
        return PopulatorMixin.matrix


