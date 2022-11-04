from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core import validators, exceptions

from apps.students.models import Option


from .choices import AvalilableOptionChoices

class AvailableOption(models.Model):
    '''
    through field between AvailableOptionChoices and Option
    '''
    option = models.ForeignKey(
        Option, 
        verbose_name=_("option connected to"), 
        on_delete=models.CASCADE
        )
    option_choices = models.ForeignKey(
        AvalilableOptionChoices, 
        verbose_name=_("available options"), 
        on_delete=models.CASCADE
        )
    classes = models.PositiveSmallIntegerField(
            verbose_name=_("classes delegated to this subject"),
            validators=[
                validators.MaxValueValidator(
                    getattr(settings, "MAX_CLASS_SIZE", 40)
                )
            ],
            blank=True,
            null=True
        )
    
    class Meta:
        verbose_name_plural = "Available Options"
        unique_together = ("option", "option_choices")
    
    def __str__(self) -> str:
        return "[%s]|%s|" % (self.option.title, self.option_choices.title)