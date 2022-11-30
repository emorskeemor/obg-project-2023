
import os

os.environ.setdefault("OBG_SETTINGS_MODULE", "settings")

import copy
import time

from bloc.static.dummy import DUMMY_DATA
from bloc.core.post_generate.validators import *

from bloc.core import Generator

from bloc.core.post_generate.operations import execute_operation


    
if __name__ == "__main__":    
    EBACC={
        "humanities":["Hi","Ge"],
        "languages":["Fr","Sn"],
        "sciences":["Sc","Co"],
        "vocational":["Co","Bs","Eg","Cb", "Hc", "Bb", "Mu", "Pb", "Sb", "Hb", "Mu"]
    }
    # system setup
    generator = Generator(
        data=DUMMY_DATA.data,
        options=DUMMY_DATA.options,
        blocks=4,
        debug=True,
        protocol=3,
        target_percentage=95.8,
        ebacc=EBACC,
        # protocol 3
        evaluation_config={
            "pathways":True,
        }
    )
    
    
    generator.setup()
    
    generator.insert_together("Bb", "Bs")
    generator.insert_together("Dr", "Pb")
    
    generator.classes_per_subject.update(
        Bb=2, Sn=3, Co=2, Mu=1, Bs=2, Py=1, Fr=2
        )

    # execution

    generator.execute()
    
    # evaluation
            
    generator.evaluate(
        validators=[
            # PerfectAlignmentValidator
            # MaxOptionsValidator(12)
        ],
        check=True,
        debug=False,
        )
        
    generator.evaluation.pprint()
    
    # print(generator.evaluation.student_paths(EBACC).serialized_groups())
    

    operation = execute_operation(
        operation="move",
        blocks=generator.evaluation.blocks,
        target=(0, "Dr"), to=1
    )
    result = operation.compare()
    print(result)