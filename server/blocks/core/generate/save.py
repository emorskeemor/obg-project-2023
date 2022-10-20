import copy
import time
from collections import deque
from itertools import permutations
from typing import Any, Dict, List, NoReturn

from blocks.core.exceptions import (ImproperlyConfigured, SavePointRequired,
                                    WatchGuardTriggered)
from blocks.core.generate.population import PopulatorMixin
from blocks.core.postgenerate.evaluation import (EvaluatedObject,
                                                 EvaluationUtility)
from blocks.core.pregenerate.statistics import group_by_class, subject_counts

from .state import STATE_PROCESS, BaseProcess, MainProcess


class SaveNode(PopulatorMixin):
    '''
    Node used for generating a set of option blocks.
    '''
    creation_counter = 0
    __best_evaluation:EvaluatedObject = None
    __best_savepoint = None
    __ordered_process:List[BaseProcess] = STATE_PROCESS
    __completed_savepoints:List = []
    cache = {}
    
    def __init__(self, blocks:List[List[str]], data:Dict[Any,List], parent=None) -> None:
        super().__init__()
        self.blocks = blocks
        self.DATA = data
        # the parent can be used to trace back
        self.parent = parent

        # DEFERED ATTRIBUTES
        self.__state:BaseProcess = None
        self.__state_pos:int = 0
        # these methods are not required on instatiation
        self.classes_per_subject:Dict = None
        # self.cache = dict()
        self.__grouped = dict()
        self.used = set()
        
        self.__evaluate = False
        self.__enable_main_sp = True

        self.together = {}

        self.__ebacc = None
        self.debug = False
        
        self.__set_creation_counter()
        self.id = self.creation_counter

    def __str__(self) -> str:
        parent = self.parent
        if parent is None:
            parent = "init"
        return "Savepoint[%i]/%s" % (self.id, parent)
    def __repr__(self) -> str:
        return self.__str__()
    
    ############# READ ONLY PROPERTIES ##############

    @property
    def completed_savepoints(self) -> List:
        '''A list of completed savepoints that are ready to be evaluated'''
        return SaveNode.__completed_savepoints

    @property
    def best_evaluation(self) -> EvaluatedObject:
        '''Returns the best evaluated object found during generation'''
        assert self.__evaluate is True, (
            "cannot get best evaluation when evaluation was disabled during generation"
            )
        return self.__best_evaluation

    @property
    def best_savepoint(self):
        '''
        save point that generated the best option block
        '''
        return self.__best_savepoint
    
    ############# PUBLIC METHODS #################
    
    def insert_together(self, target:str, *others:object, max_uses:int=None):
        '''
        defines a target subject that whenever is about to be inserted, must be inserted
        with a given set of subjects. The max use of this rule can be defined but it 
        by default uses the required classes per subject
        '''
        if max_uses is None:
            max_uses = self.classes_per_subject.get(target, None)
        assert max_uses is not None, (
            "Could not find the max use of '%s' in required dictionary" % target
            )
        self.together.update({target:(others, max_uses)})

    def new_node(self):
        '''
        Create a new node
        '''
        blocks = copy.deepcopy(self.blocks)
        # create new save node and set some attributes
        node = SaveNode(blocks, self.DATA, parent=self)
        
        node.classes_per_subject = copy.copy(self.classes_per_subject)
        node.used = copy.copy(self.used)
        node.__evaluate = self.__evaluate
        # node.cache = copy.copy(self.cache)
        node.together = copy.deepcopy(self.together)

        node.__enable_main_sp = self.__enable_main_sp
        node.__ebacc = self.__ebacc

        node.__grouped = self.__grouped
        # ensure state is copied over
        node.__state = self.__state
        node.__state_pos = self.__state_pos
        node.debug = self.debug
        return node
    
    def enable_evaluation(self, ebacc:Dict):
        '''
        evaluation will take place during generation
        '''
        self.__evaluate = True
        self.__ebacc = ebacc

    def disable_main_savepoints(self):
        '''
        save points during the main process will be disabled
        '''
        self.__enable_main_sp = False

    def next_process(self):
        '''
        returns the next process that in the generation process
        '''
        self.__state_pos += 1        
        if self.__state_pos >= len(self.__ordered_process):
            return False    
        self.__state = self.__ordered_process[self.__state_pos]
        
        return True
    
    def run(self):      
        '''
        recurive method to generate blocks. Calls itself when it is able to move onto
        the next process
        '''  
        # print("current process:", self.__state)
        # print("run called :", self.blocks)
        # time.sleep(1)
        try:
            # instantiate the next process and run it
            self.__ready_process().run_process()
            if self.next_process() is True:
                # move onto the next process through recursion
                self.run()
            else:
                # either evaluate on the spot or save to an array.
                if self.__evaluate:
                    self.__evaluate_blocks()
                else:
                    self.__display("resolved node :", self) 
                self.__append_complete(self)    
        except SavePointRequired as sp:
            # a savepoint was required and was raised from the process. For each option,
            # cre ate a new node and insert
            # print("\nSP REQUIRED :", sp.options, sp.subject_code)
            for opt in sp.options:
                node = self.new_node()
                # we only want to run the node if the forced insertion  
                # commited otherwise it will loop infinitely with no state change
                if node.populate_block(sp.subject_code, opt) is True:
                    # print("\nnew savepoint ran")
                    node.run()
                
                    
    def check(self, raise_exceptions=True) -> List:
        '''
        check to see if there are no problems before running generation
        '''
        errors = []
        for subject, required_count in self.classes_per_subject.items():
            _, count = self.__grouped.get(subject)
            if count != required_count and required_count > len(self.blocks):
                
                error = ImproperlyConfigured(
                    "subject '%s' has been set to have a number of classes greater " % subject + 
                    "than the number of option blocks required"
                )
                if raise_exceptions is True:
                    raise error
                errors.append(errors)
        return errors
    
    def resolve(self):
        '''
        yields all parents of savenode
        '''
        current_node = self
        yield current_node
        while current_node.parent is not None:
            yield current_node
            current_node = current_node.parent
                               
    ############# PRIVATE METHODS #################

    def __ready_process(self) -> BaseProcess:
        # instantiate the current process and get it ready to run
        args = (
            self.blocks, self.DATA,
            self.__class__.cache, self.classes_per_subject, self.used,
            self.__grouped, self.together, self.__enable_main_sp
            )
        init:BaseProcess = self.__state(*args)
        if self.__enable_main_sp is False and isinstance(init, MainProcess):
            init.enable_sp = False 
        return init

    def _setup(self, opt_codes, class_size):
        # set up does not need to be called on every creation of a save point.
        # it only needs to be called on initial generation to calculate certain 
        # values
        _subject_counts = subject_counts(self.DATA, option_codes=opt_codes)
        self.__grouped = group_by_class(_subject_counts, class_size)
        if self.classes_per_subject is None:
            self.classes_per_subject = {
                subject:useage[1] for subject, useage in self.__grouped.items()
                }
        
        self.__state = self.__ordered_process[0]
        self.__state_pos = 0

    def __set_creation_counter(self):
        self.creation_counter = SaveNode.creation_counter
        SaveNode.creation_counter += 1

    def __append_complete(self, savepoint):
        SaveNode.__completed_savepoints.append(savepoint)
    
    def __evaluate_blocks(self):
        # evaluate current blocks. If the current evaluation is greater than the best,
        # it becomes the new best
        evaluated = EvaluationUtility(self.DATA, self.blocks, self.__ebacc)
        evaluated.evaluate_pathways = False
        evaluated.execute()
        eval_obj = evaluated.evaluation
        best_evaluation = SaveNode.__best_evaluation
    
        if best_evaluation is None or eval_obj.success_percentage > best_evaluation.success_percentage:
            SaveNode.__best_evaluation = evaluated.evaluation
            SaveNode.__best_savepoint = self

    def __display(self, *args, **kwargs) -> NoReturn:
        if self.debug:
            print(*args,**kwargs)
                        
