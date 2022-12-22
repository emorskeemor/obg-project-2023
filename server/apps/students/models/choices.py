from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models

from .options import Option
from .students import Student


class Choice(models.Model):
    '''
    Through field between student and option
    '''
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="choices")
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="choices")
    reserve = models.BooleanField(verbose_name=_("declares if the choice is a reserve"), default=False)
    priority = models.PositiveIntegerField(verbose_name=_("priority of the option"), default=0)

    def __str__(self) -> str:
        return "%s => %s" % (self.student, self.option)

    # def clean(self) -> None:
    #     # fail safe to ensure there are no duplicate relationships
    #     if Choice.objects.filter(student=self.student, option=self.option).exists():
    #         raise ValidationError(
    #             "cannot add as student already has this subject as an option"
    #             )
    #     return super().clean()

    def save(self, *args, **kwargs):
        super(Choice, self).save(*args, **kwargs) 