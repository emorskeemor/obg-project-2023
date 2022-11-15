from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.environment.models import GenerationSettings
from apps.students.models import Option

class InsertTogether(models.Model):
    '''
    defines subjects that must be inserted when a target subject is inserted
    '''
    target = models.ForeignKey(
        Option, 
        verbose_name=_("target option"), 
        on_delete=models.CASCADE,
        related_name="targets"
        )
    settings = models.ForeignKey(
        GenerationSettings, 
        verbose_name=_("settings connected to"), 
        on_delete=models.CASCADE
        )
    
    targets = models.ManyToManyField(
        Option, 
        verbose_name=_("target subjects")
        )
    
    class Meta:
        verbose_name_plural = "Insert together"
    
    def __str__(self) -> str:
        return "[%s](%s)" % (self.settings.title, self.target.title)