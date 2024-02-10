from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.conf import settings

from .rooms import Room

class GenerationSettings(models.Model):
    '''
    settings for generation that can be saved
    '''
    # the room that the settings is linked to
    room = models.OneToOneField(
        Room,
        on_delete=models.CASCADE,
        verbose_name=_("room connected to"),
        related_name="settings"
    )
    # the title of the settings
    title = models.CharField(
        max_length=50,
        verbose_name=_("name of settings")
        )
    # constraints and settings
    blocks_must_align = models.BooleanField(default=False)
    max_subjects_per_block = models.PositiveIntegerField(
        default=20,
        validators=[
            validators.MaxValueValidator(30),
        ]
    )
    # number of blocks 
    blocks = models.PositiveIntegerField(
            default=4,
            validators=[
                validators.MaxValueValidator(12),
            ],
        verbose_name=_("number of option blocks")
        )
    # max class size
    class_size = models.PositiveIntegerField(
            default=getattr(
                settings, "DEFAULT_CLASS_SIZE", 24
            ),
            verbose_name=_("max class size"),
            validators=[
                validators.MaxValueValidator(
                    getattr(settings, "MAX_CLASS_SIZE", 40)
                )
            ]
        )
    lesson_cost = models.FloatField(
        verbose_name=_("cost per lesson"),
        default=5000
        )
    
    class Meta:
        verbose_name_plural = "Settings"
        unique_together = ("room", "title")
    
    def __str__(self) -> str:
        return "%s [%s] <settings>" % (self.room, self.title)
