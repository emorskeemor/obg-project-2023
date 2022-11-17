from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core import validators

from apps.students.models import Option
from apps.environment.models import Room


class AvalilableOptionChoices(models.Model):
    '''
    available options available for a given room
    '''
    title = models.CharField(_("preset title"), max_length=50)
    options = models.ManyToManyField(
        Option, 
        through="AvailableOption",
        verbose_name=_("available options"),
        related_name="available_option_choices"
        )
    room = models.OneToOneField(
        Room,
        on_delete=models.CASCADE,
        null=True,
        related_name="available_option_choices",
        blank=True,
    )
    
    class Meta:
        verbose_name_plural = "Available Option Choices"
        unique_together = ["room","title"]
        
    def __str__(self) -> str:
        return "%s <opts>" % (self.title)