from typing import List, Tuple


class OBGError(Exception):
    '''
    base exception for all obg errors
    '''



class EvaluationFailed(OBGError):
    '''
    an error occured during an evaluation process
    '''
    def __init__(self, *args: object, **details) -> None:
        super().__init__(*args)
        self.details = details

class PriorityFailed(OBGError):
    '''
    raised when a priority is failed
    '''
    def __init__(self, *args: object, **details) -> None:
        super().__init__(*args, **details)

class NonExistentObject(OBGError):
    '''
    generall object does not exist
    '''
    pass

class SubjectNotFound(NonExistentObject):
    '''
    requested subject could not be found
    '''
    pass

class SubjectAlreadyExists(OBGError):
    '''
    subject already exists
    '''
    pass

class PathwayFailed(OBGError):
    '''
    pathway conditions were not met
    '''
    pass

class ImproperlyConfigured(OBGError):
    '''
    the system was improperly configured leading to an error
    '''
    pass

class ValidationError(OBGError):
    '''
    error occured during validation
    '''

class WatchGuardTriggered(OBGError):
    '''
    watch guard triggered when inserting a subject
    '''
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.block_state = []
        self.save_node = None
        self.subject = None
        self.block = None
        
    def __str__(self) -> str:
        return "subject '%s' entered block '%i' while watching" % (self.subject, self.block)
        
    def display_trigger(self):
        print("\nBlock state of trigger")
        for b in self.block_state:
            print(b)
            
        print("Save node of trigger :", self.save_node)
        
class SavePointRequired(OBGError):
        
    def __init__(self, *args: object, options:List[int]=None, subject_code:str=None) -> None:
        super().__init__(*args)
        self.options =  options
        self.subject_code = subject_code
        self.state = dict()

    def __str__(self) -> str:
        return "SavePointRequired('%s')[%s]" % (self.subject_code, ",".join(map(str, self.options)))
