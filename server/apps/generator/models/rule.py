from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core import validators

from apps.environment.models import Room
from apps.students.models import Option

class InsertTogether(models.Model):
    
    target = models.ForeignKey(
        Option, 
        verbose_name=_("target option"), 
        on_delete=models.CASCADE,
        related_name="targets"
        )
    settings = models.ForeignKey(
        Room, 
        verbose_name=_(""), 
        on_delete=models.CASCADE
        )
    
    targets = models.ManyToManyField(
        Option, 
        verbose_name=_("target subjects")
        )
    
    def __str__(self) -> str:
        return "%s[%s]" % (self.settings.title, self.target.title)