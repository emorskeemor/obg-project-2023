from django.db import models
from django.core.exceptions import ValidationError
from .students import Student
from .options import Option

class Choice(models.Model):
    '''Through field between student and option'''
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "%s => %s" % (self.student, self.option)

    def clean(self) -> None:
        # fail safe to ensure there are no duplicate relationships
        if Choice.objects.filter(student=self.student, option=self.option).exists():
            raise ValidationError(
                "cannot add as student already has this subject as an option"
                )
        return super().clean()

    def save(self, *args, **kwargs):
        super(Choice, self).save(*args, **kwargs) 