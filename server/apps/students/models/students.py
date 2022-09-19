from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

import uuid

from apps.environment.models import Room

from .options import Option

class Student(models.Model):
    uuid = models.UUIDField(_("student uuid"), default=uuid.uuid4, editable=False)
    # details about student
    email = models.EmailField(_("student email"), max_length=100)
    first_name = models.CharField(_("student first name"), max_length=100)
    last_name = models.CharField(_("student last name"), max_length=100)
    # room the student is linked too
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        verbose_name=_("room connected to"),
        blank=True,
        null=True,
        )
    options = models.ManyToManyField(Option, through="Choice", related_name="students")

    def __str__(self) -> str:
        return "%s\%s" % (self.email, self.room.domain)