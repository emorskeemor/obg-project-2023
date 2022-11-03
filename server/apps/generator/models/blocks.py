from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core import validators

from apps.environment.models import Room
from apps.students.models import Option


    

class OptionBlocks(models.Model):
    
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
    
    def __str__(self) -> str:
        return "%s[%s]" % (self.room, self.title)
    
    def save(self, *args, **kwargs):
        if self.title is None:
            self.title = "%s[%i]" % (self.title, self.pk)
        super(OptionBlocks).save(*args, **kwargs)
        
class Block(models.Model):
    '''
    represents a single block connected to a given set of option blocks
    '''
    options = models.ManyToManyField(
        Option,
        verbose_name=_("options connected to the block")
        
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
        on_delete=models.CASCADE
        )
    
    def __str__(self) -> str:
        return "%s[%s]" % (self.blocks.title, self.block_id)