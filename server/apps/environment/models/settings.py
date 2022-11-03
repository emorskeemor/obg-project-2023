from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core import validators

from .rooms import Room

class GenerationSettings(models.Model):
    
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        verbose_name=_("room connected to")
    )
    title = models.CharField(
        max_length=50,
        verbose_name=_("name of settings")
        )
    
    blocks_must_align = models.BooleanField(default=False)
    max_subjects_per_block = models.PositiveIntegerField(
        default=12,
        validators=[
            validators.MaxValueValidator(30),
        ]
    )
    blocks = models.PositiveIntegerField(
            default=4,
            validators=[
                validators.MaxValueValidator(12),
            ],
        verbose_name=_("number of option blocks")
        )
    
    def __str__(self) -> str:
        return "%s settings" % self.room.title
    