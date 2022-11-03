from django.db import models
from django.core import validators
from django.utils.translation import gettext_lazy as _

from apps.students.models import Option
from apps.environment.models import Room

class Requirement(models.Model):
    '''
    represents a requirement that the student must obtain in order to take this given subject.
    '''
    # this can be different for different rooms he hence why it is a model
    
    grade = models.IntegerField(
        verbose_name=_("grade required"),
        default=4,
        validators=[
            validators.MaxValueValidator(10),
            validators.MinValueValidator(0)
        ]
        )
    
    subject = models.ForeignKey(
        Option, 
        on_delete=models.CASCADE,
        verbose_name=_("subject requirement")
        )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        verbose_name=_("room connected to")
    )
    
    def __str__(self) -> str:
        return "%s[%i] => %s" % (
            self.subject.title,
            self.grade,
            self.room
        )
    
    