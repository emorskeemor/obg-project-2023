import uuid

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _


class Option(models.Model):
    '''
    represents an option that a student can choose
    '''
    uuid = models.UUIDField(_("student uuid"), default=uuid.uuid4, editable=False)
    title = models.CharField(_("subject name"), max_length=100)
    subject_code = models.CharField(_("subject code"), max_length=2, blank=True)
    description = models.TextField(max_length=400, blank=True)
    slug = models.SlugField(max_length=250, blank=True)
    requirements = models.CharField(
        _("subject requirements"), 
        max_length=50,
        blank=True
        )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if not self.subject_code:
            self.subject_code = self.title[:2]
        super(Option, self).save(*args, **kwargs) 

    def __str__(self) -> str:
        return "%s, %s" % (self.title, self.subject_code)