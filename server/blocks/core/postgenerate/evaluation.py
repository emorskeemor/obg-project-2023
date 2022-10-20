import copy
from typing import Any, Dict, Iterable, List, NoReturn, Tuple

from blocks.core.pregenerate.statistics import subject_block_count

from ..exceptions import (EvaluationFailed, ImproperlyConfigured,
                          PathwayFailed, PriorityFailed, ValidationError)
from .pathway import DEFAULT_PATHWAYS, BasePathway


class EvaluatedObject:
    '''
    An evaluation of set of a option blocks
    '''
    def __init__(self) -> None:
        self.failed_options: Dict[str, Dict] = dict()
        self.successful_options: Dict[str, Dict] = dict()
        self.blocks: List[List] = []
        self.total_students = 0
        self.evaluated = False
        self.success_percentage:float = 0
        self.__paths_enabled = True

    def __str__(self) -> str:
        return "<EvaluatedObject>"

    def __repr__(self) -> str:
        return self.__str__()

    def display_sucessful(self):
        '''
        display pretty format of successful subjects to stdout
        '''
        # pretty print the id, built options and the route the student is taking
        for key, data in self.successful_options.items():
            details = data["options"]
            print("\nID:(%s) |%s|" % (key,
                ",".join(["%s:[%s]" % (code, block) for code, block in sorted(details, key=lambda x:x[1])]),
            ))
            print("Pathway : %s" % str(data["pathway"]))

    def display_failed(self):
        '''
        display pretty format of failed subjects to stdout
        '''
        # pretty print the failed options by displaying the id, initial options
        # and the errors
        for key, error_data in self.failed_options.items():
            exceptions = error_data["exceptions"]
            print("\n<ID:(%s) inital options: [%s]" % (
                    key, ",".join(error_data["initial_options"])
                    ))   
            for exception in exceptions:
                print("> %s" % str(exception))
        print("\nFailed options : %i" % len(self.failed_options))

    def order_sucess_options(self):
        '''
        orders successful students options by block order
        '''
        for data in self.successful_options.values():
            options = data.get("options")
            # order the options by block number from 1-4
            data["options"] = sorted(options, key=lambda x:x[1])
        return self.successful_options

    def _set_success_percentage(self):
        # assert to avoid a zero error
        assert self.total_students, "total students must not equal to 0"
        success = len(self.successful_options)
        self.success_percentage = round(success/self.total_students*100, 2)

    def filter_by_path(self, path_name:str):
        @staticmethod
        def _path_filter(item):
            pathway = item[1]["pathway"]
            assert isinstance(pathway, BasePathway), "found a path that is not an instance of 'BasePathWay'"
            return pathway.pathway_name == path_name
        return list(filter(_path_filter,self.successful_options.items()))

        
    def display_evaluation(self):
        """
        pretty print evaluation to stdout
        """
        print("Total generation statistics :")
        print("\nTotal options : %i" % self.total_students)
        print("Successful options : %i" % len(self.successful_options))
        print("Failed options : %i" % len(self.failed_options))
        print("Success percentage : %f %%" % self.success_percentage)
        print("\nblocks generated :")
        
        for b in self.blocks:
            print(b)
                


class EvaluationUtility:
    '''
    Evaluation utility to evalute a set of data against a set of blocks
    '''    
    # the order in which we check these paths matter as people on path four
    # did not follow any of the paths
    default_pathways:List[BasePathway] = DEFAULT_PATHWAYS

    def __init__(self, data:Dict[Any, List], blocks:List[List], ebacc_subjects:Dict[str,Dict]=None, **options: object) -> None:
        # copy data and blocks 
        self.data = copy.deepcopy(data)
        self.blocks = blocks
        self.options: Dict = options
        self.ebacc_subjects = ebacc_subjects 
        self.evaluation: EvaluatedObject = None
        
        # evaluation options
        self.evaluate_pathways = True
        self.max_subjects_per_block = 12
        self.blocks_must_align = False
        

    def try_against_blocks(self, options:List, order=True, raise_exceptions=True, prioritise:int=None) -> List[Tuple[str,int]]:
        '''
        try a set of options against the given set of blocks. set order
        to false to prioritise the initial order instead of automatically ordering.
        '''
        # deep copy blocks and options as we are going to be manipulating them
        # but we need to make sure we still have an untouched version for other options
        blocks = copy.deepcopy(self.blocks)
        options = copy.deepcopy(options)
        # order blocks by number of available subjects
        required_iters = len(options)
        current_iters = 0
        handled = []
        # iterate until the length of subjects have been dealt with
        while current_iters < required_iters:
            counts = subject_block_count(options, blocks)
            # decide whether to order the counts or not. We want to do this
            # when prioritising a level of choices by original order
            if order:
                subject, count = [
                    (subj,occ) for subj, occ in sorted(counts.items(), key=lambda x:x[1])
                    ][0]
            else:
                subject, count = list(counts.items())[0]
            if count == 0:
                # if the count is 0, it means that the option could not be found in
                # the option blocks. This could be due to another subject already
                # taking up an option block.
                if prioritise is not None:
                    assert type(prioritise) is int, "prioritise must be an integer"
                    if prioritise > len(handled):
                        raise PriorityFailed(
                            "unable to match options against priority level")
                if raise_exceptions:
                    raise EvaluationFailed(
                        "%s could not be evaluated" % subject,
                        subject=subject
                    )
            # iterate through each block and try and insert the subject
            for block, subjects in enumerate(blocks):
                # check that the block has not already been dealt with
                if subjects is not None and type(subjects) is list:
                    if subject in subjects:
                        # if the subject is found, we have dealt with a subject
                        # and we need to set the block we found it in to be unusable
                        # and get detail about what we did with the subject
                        handled.append((
                            subject,
                            block+1
                        ))
                        blocks[block] = None
                        break

            options.remove(subject)
            current_iters += 1

        if raise_exceptions:
            # saftey net
            assert len(handled) == required_iters, "unmatched handled subjcts"
        return handled

    def get_pathway(self, options:List[str]):
        '''
        returns the pathway a set of options follow
        '''
        pathways:List[BasePathway] = self.options.get("pathways", self.default_pathways)
        for possible_path in pathways:
            try:
                path = possible_path(self.ebacc_subjects)
                return path(*options)
            except PathwayFailed:
                pass
        # raise an error meaning that the path ways we provided resulted in no
        # fallback pathway to be found
        raise ImproperlyConfigured("could not find a general pathway for this object")

    def prioritise_failed(self, options:List[str], level=2):
        '''
        evaluate failed options by prioritising their original order
        '''
        # we know that these options will not evaluate sucessfully but we
        # can at least priorities a certain number of subjects that are in
        # order
        try:
            return self.try_against_blocks(
                options, 
                order=False, 
                raise_exceptions=False,
                prioritise=level
                )
        except PriorityFailed as failed:
            # if this occurs, it means that we could not priories the level
            # of options specified which can be a raise for concern to the end
            # user
            return failed
        
    def execute(self):
        '''
        execute evaluation utility
        '''
        # create a new evaluation instance to store results
        if self.evaluate_pathways is True:
            assert self.ebacc_subjects is not None, "evaluating pathways requires ebacc subjects to be provided"
        
        evaluation = EvaluatedObject()
        evaluation.total_students = len(self.data)
        # iterate through each set of student options
        for key, student_options in self.data.items():
            try:
                opts = self.try_against_blocks(student_options)
                pathway = self.get_pathway(student_options) if self.evaluate_pathways else None
                
                evaluation.successful_options.update({
                    key:{
                        "options":opts,
                        "pathway":pathway
                    }
                })
            except EvaluationFailed as failure:
                # if the evaluation failed, log why it failed
                errors = [failure]
                prioritised = self.prioritise_failed(student_options)
                if isinstance(prioritised, EvaluationFailed):
                    errors.append(prioritised)
                    prioritised = None
                evaluation.failed_options.update({ 
                    key:{
                        "initial_options":student_options, 
                        "priorities": prioritised,
                        "exceptions": errors
                    }}
                )
        evaluation._set_success_percentage()
        evaluation.blocks = self.blocks
        # set evaluated flag to true to ensure all processes have been completed
        evaluation.evaluated = True
        self.evaluation = evaluation

    def __str__(self) -> str:
        return "<EvaluationUtility>"

    def __repr__(self) -> str:
        return "<EvaluationUtility>"

        
    def calculate_pathways(self, data:Dict[Any, List]):
        for item, options in data.items():
            yield item, self.get_pathway(options)
                
    def check(self, raise_exceptions=False):
        '''
        check if the set of option blocks satisfy options
        '''
        assert self.evaluation.evaluated is True, "cannot check an unevaluated object"
        
        # max subjects per block
        try:
            self.__check_max_subject_per_block()
            self.__check_perfect_alignment()
        except ValidationError as error:
            if raise_exceptions:
                raise error
            return False
        return True
        
        
    
    ############# PRIVATE METHODS #############
    
    def __check_max_subject_per_block(self):
        # checks that the number of subjects in each block is less than a 
        # certain maximum
        for block in self.evaluation.blocks:
            if len(block) > self.max_subjects_per_block:
                raise ValidationError(
                    "too many subjects in one block"
                )
                
    def __check_perfect_alignment(self):
        # validates that the number of subjects in each block must be the same
        if self.blocks_must_align:
            res = {len(block) for block in self.evaluation.blocks}
            if len(res) != 1:
                raise ValidationError(
                    "number of subjects in each block did not perfectly algin"
                )
    