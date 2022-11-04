from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core import validators

from apps.students.models import Option

from .rooms import Room


    
    
class AvalilableOptions(models.Model):
    '''
    available options available for a given room
    '''
    title = models.CharField(_("preset title"), max_length=50)
    options = models.ManyToManyField(
        Option, 
        through="AvailableOption",
        verbose_name=_("available options"),
        )
    room = models.ForeignKey(
        Room, 
        verbose_name=_("room connected to"), 
        on_delete=models.CASCADE,
        related_name="rooms"
        )
    
    class Meta:
        verbose_name_plural = "available options"
    
    def __str__(self) -> str:
        return "%s [%s] <opts>" % (self.room, self.title)
    
class AvailableOption(models.Model):
    
    option = models.ForeignKey(
        Option, 
        verbose_name=_("option connected to"), 
        on_delete=models.CASCADE
        )
    available_options = models.ForeignKey(
        AvalilableOptions, 
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