from typing import Dict, List

from blocks.core.exceptions import PathwayFailed

# ebacc = {
#   humanities : [...],
#   sciences : [...],
#   languages : [...],
# }

class BasePathway:
    '''
    calling an instance of a pathway validates it and if successful, returns the
    pathway 
    '''

    summary_message = "message"
    pathway_name = None
    
    def __init__(self, ebacc_subjects:Dict[str, List]) -> None:
        self.ebacc = ebacc_subjects
        self.sciences:List = self.get_category("sciences")
        self.humanities:List = self.get_category("humanities")
        self.languages:List = self.get_category("languages")
        self.vocational:List = self.get_category("vocational")
        self.pathway_name = self.__class__.__name__

    def __str__(self) -> str:
        return "%s[%s]" % (self.__class__.__name__, self.summary_message)

    def __repr__(self) -> str:
        return self.__str__()

    def validate(self, *options):
        raise NotImplementedError("pathway validate() not implmented")

    def get_category(self, category:str):
        subjects = self.ebacc.get(category, None)
        if subjects is None:
            raise KeyError(
                "could not find '%s' category in ebacc subjects" % subjects
                )
        if type(subjects) is not list:
            raise TypeError(
                "subjects value for '%s' must be type list" % category
            )
        return subjects

    

    def __call__(self, *options):
        self.validate(*options)
        return self

class PathOne(BasePathway):
    '''
    Students who wish to follow a more academic path of Alevels followed by university. This
    pathway maintains access to all career paths.

    Students must pick Geography or History (or both), a language and then have two free choices.
    '''
    summary_message = "Full EBacc"

    def validate(self, *options):
        # to be eligible for this route, the student must have ONE subject from humanities,
        # a science and a language.
        check = dict.fromkeys(["sciences","languages","humanities"], False)
        for option in options:
            for category in check.keys():
                if option in self.get_category(category):
                    check[category] = True
        if not all(check.values()):
            raise PathwayFailed

class PathTwo(BasePathway):
    '''
    Students whose career path is supported by vocational options. At the end of key
    stage 4, they would consider a vocational course or workrelated learning.

    Agreed by the student’s Form Tutor. Students must still pick one EBacc subject (geography, history, 
    triple science, computer science, ora language), a vocational subject and then have two free choices.
    '''

    summary_message = "Vocational Route"
    
    def validate(self, *options):
        # as long as they have an EBACC AND a VOCATIONAL subject then they
        # eligible for this route
        vocational = False
        ebacc = False
        for option in options:
            if option in self.sciences + self.humanities + self.languages:
                ebacc = True
            elif option in self.vocational:
                vocational = True
        if vocational is False or ebacc is False:
            raise PathwayFailed


class PathThree(BasePathway):
    '''
    Students who have additional needs for whom four options may create a work overload. 

    Students are invited to follow this path by our SENCO and Head of Year. Students should aim 
    for one EBacc subject and then have two free choices. The fourth option is supervised
    study
    '''

    summary_message = "SENCO Exception"

    def validate(self, *options):
        if len(options) != 3:
            raise PathwayFailed

class PathFour(BasePathway):
    '''
    fallback route if other student choice's were not eligible for their route
    '''

    summary_message = "Non-route"

    def validate(self, *options):
        pass


DEFAULT_PATHWAYS:List[BasePathway] = [PathOne, PathTwo, PathThree, PathFour]

