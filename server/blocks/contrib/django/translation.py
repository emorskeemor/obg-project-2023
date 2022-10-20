
from typing import Dict, List

from django.db import models


def get_student_options(model:models.Model, room_code) -> List[Dict[int|str, List[str]]]:
    queryset = model.objects.filter(room_code=room_code)
    
    