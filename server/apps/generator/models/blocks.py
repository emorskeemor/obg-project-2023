from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import validators

from apps.environment.models import Room
from apps.students.models import Option


    

class OptionBlocks(models.Model):
    '''
    option blocks that have been saved
    '''
    class Meta:
        verbose_name_plural = "Option blocks"
        unique_together = ("room", "title")
    
    room = models.ForeignKey(
        Room, 
        verbose_name=_("room connected to"), 
        on_delete=models.CASCADE
        )
    title = models.CharField(max_length=50, blank=True, null=True)
    number_of_blocks = models.PositiveIntegerField(
        _("number of blocks"),
        validators=[
            validators.MaxValueValidator(
                getattr(settings, "MAX_BLOCKS", 15)
            )
        ]
        )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="option_blocks",
        null=True
    )
    success_percentage = models.FloatField(default=0)
    generation_time = models.FloatField(default=0)
    completed_nodes = models.PositiveIntegerField(default=0)
    generated_nodes = models.PositiveIntegerField(default=0)
    
    def __str__(self) -> str:
        return "%s[%s]" % (self.room.code, self.title)
    
    def save(self, *args, **kwargs):
        if self.title is None:
            self.title = "%s[%i]" % (self.title, self.pk)
        super().save(*args, **kwargs)
        
class Block(models.Model):
    '''
    represents a single block connected to a given set of option blocks
    '''
    options = models.ManyToManyField(
        Option,
        verbose_name=_("options connected to the block"),
        related_name="options"
        )
    number_of_subjects = models.IntegerField(
        _("number of subjects")
        )
    block_id = models.PositiveIntegerField(
        _("block id"),
        validators=[
            validators.MaxValueValidator(
                getattr(settings, "MAX_BLOCKS", 15)
            )
        ]
        )
    blocks = models.ForeignKey(
        OptionBlocks, 
        verbose_name=_("set of blocks connected to"), 
        on_delete=models.CASCADE,
        related_name="blocks"
        )
    
    def __str__(self) -> str:
        return "%s[%s] <%s>" % (self.blocks.title, self.block_id, self.blocks.room.code, )