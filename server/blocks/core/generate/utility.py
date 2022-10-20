import time
from typing import Any, Dict, List

from blocks.core import STATIC_ROOT
from blocks.core.exceptions import ImproperlyConfigured, WatchGuardTriggered
from blocks.core.generate.population import PopulatorMixin
from blocks.core.postgenerate.evaluation import (EvaluatedObject,
                                                 EvaluationUtility)

from .save import SaveNode


class State:
    READY = "READY"
    UNPREPARED = "UNPREPARED"
    COMPLETED = "COMPLETED"
    RUNNING = "RUNNING"
    EVALUATED = "EVALUATED"


class Generator:
    '''
    Generator utility to generate option blocks
    methods to run in order
    
    prepare_generation() -> creates a savenode and sets it up with the given parameters.
    You are then able to overide certain settings before generation occurs
    
    run_generation() -> no more settings can be changed and the generation process is run.
    
    evaluate_generation() -> evaluates the save nodes created and finds the one with the
    best success %
    
    certain methods/properties cannot be accessed until certain methods have been called
    '''
    state = State
    
    def __init__(self, data:Dict[Any, List], options_codes:List[str], num_blocks:int, class_size:int=24) -> None:
        self.data = data
        self.option_codes = options_codes
        self.num_blocks = num_blocks
        self.class_size = class_size
        self.generation_state = "unprepared"
        self.node:SaveNode = None
        self.__debug = False
        self.__best_evaluation = None
        self.__best_savepoint = None
        self.blocks_must_align = False
        self.max_subjects_per_block = 12
        
        
    @property
    def best_evaluation(self) -> EvaluatedObject:
        '''
        returns the best evaluated object
        '''
        self.__check_evaluation_completed()
        return self.__best_evaluation
    
    @property
    def best_savepoint(self) -> SaveNode:
        '''
        returns the best save point that generated the best option blocks
        '''
        self.__check_evaluation_completed()
        return self.__best_savepoint
            
    def insert_together(self, target:str, *subjects, max_uses:int=None):
        '''
        defines a target subject that whenever is about to be inserted, must be inserted with a 
        given set of subjects. The max use of this rule can be defined but it by 
        default uses the required classes per subject
        '''
        # proxy the save node
        self.__check_prepare_completed()
        self.node.insert_together(target, *subjects, max_uses=max_uses)
    
    def prepare_generation(self) -> SaveNode:
        '''
        prepares the SaveNode class for option block generation
        '''
        blocks = [[] for _ in range(self.num_blocks)]
        util = SaveNode(blocks, self.data)
        util._setup(self.option_codes, self.class_size)
        util.debug = self.__debug
        self.node = util
        self.generation_state = self.state.READY
        self.__display("generator ready")
                
    def run_generation(self):
        '''
        executes the evaluation process
        '''
        self.node.check()
        self.__check_prepare_completed()
        start = time.perf_counter()
        self.generation_state = self.state.RUNNING
        self.__display("running generator")
        try:
            self.node.run()   
            self.generation_state = self.state.COMPLETED
        except KeyboardInterrupt:
            print("generation cancelled by user")
        end = time.perf_counter()
        self.__display(f"\ntime taken to generate blocks : {end-start}")
        
    
    def evaluate_generation(self, ebacc=None):
        '''
        goes through the evaluated savenodes of the savenode class and returns the
        evaluation with the best success percentage
        '''
        self.__check_run_completed()
        self.__display(f"evaluating '{len(self.node.completed_savepoints)}' completed save points")
        start = time.perf_counter()
        best = None
        for sp in self.node.completed_savepoints:
            # use the evaluation utility for each savepoint and evaluate individually
            util = EvaluationUtility(self.data, sp.blocks, ebacc)
            # util.evaluate_pathways = False
            util.blocks_must_align = self.blocks_must_align
            util.max_subjects_per_block = self.max_subjects_per_block
            
            if ebacc is None:
                # disable pathway evaluation if no ebacc subjects were provided
                util.evaluate_pathways = False
            util.execute()
            # we need to check if the set of blocks matches are given criteria. The check() method
            # will tell us if we can discard this set of options as it does not follow the rules provided
            if not util.check():
                continue
            if best is None or (util.evaluation.success_percentage > best.success_percentage):
                best = util.evaluation
                self.__best_savepoint = sp
        end = time.perf_counter()
        self.__display(f"\ntotal evaluation time taken : {end-start}")
        self.__display("done!")
        self.__best_evaluation = best
        self.generation_state = self.state.EVALUATED
        return best
    
    
    def display_evaluation(self):
        '''
        pretty print evaluation
        '''
        self.__check_evaluation_completed()
        self.best_evaluation.display_evaluation()
    
    def update_classes_per_subject(self, **kwargs):
        '''
        overide the classes delegated to each subject
        '''
        self.__check_prepare_completed()
        self.node.classes_per_subject.update(**kwargs)
        
    def is_successful(self):
        '''returns bool whether or not generation state is completed'''
        return self.generation_state == self.state.COMPLETED
    
    def __check_prepare_completed(self):
        if self.generation_state != self.state.READY:
            raise ImproperlyConfigured(
                "unavailable until prepare_generation() method is called"
            )
            
    def __check_run_completed(self):
        if self.generation_state != self.state.COMPLETED:
            raise ImproperlyConfigured(
                "unavailable until run_generation() method is called"
            )
            
    def __check_evaluation_completed(self):
        if self.generation_state != self.state.EVALUATED:
            raise ImproperlyConfigured(
                "unavailable untill evaluate_generation() method is called"
            )
                        
    def debug(self):
        '''enable debug mode'''
        self.__debug = True
    
    def __display(self, msg:str):
        if self.__debug:
            print(msg)
            
