

from typing import Iterable, List

from blocks.core.exceptions import ValidationError


class BaseOptionValidator:

    def check(self, options:Iterable):
        raise NotImplementedError(
            "check method not implemented"
        )
        
    def __call__(self):
        return self.check()
    

class DistinctValidator(BaseOptionValidator):
    
    def __init__(self, *subjects) -> None:
        self.subjects = subjects
    
    def check(self, options:Iterable):
        opts = set(options)
        opts.update(self.subjects)
        if len(opts) == len(options):
            raise ValidationError(
                "options contains subjects that may not co-exist"
            )
    
# class MaxSubjectUseValidator(BaseOptionValidator):
#     subject_uses = dict()
#     def __init__(self, subject, max_use) -> None:
#         super().__init__()
#         self.__class__.subject_uses.update({subject:0})
#         self.subject = subject
#         self.max_use = max_use
        
#     def check(self, options:Iterable):
#         klass = self.__class__
#         if self.subject in options:
#             count = klass.subject_uses.get(self.subject)
#             if count > self.max_use -1:
#                 raise ValidationError(
#                     "max use of this subject has already been used"
#                 )
                
#             klass.subject_uses[self.subject] = count + 1
#         print(klass.subject_uses)
        
class OptionsValidator:
    def __init__(self) -> None:
        self.validators:List[BaseOptionValidator] = []
        
    def use(self, validator):
        self.validators.append(validator)
        
    def validate(self, *options):
        for validator in self.validators:
            validator.check(options)