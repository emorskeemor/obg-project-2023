from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

import random 
import string

ROOM_CODE_LENGTH = getattr(settings, "ROOM_CODE_LENGTH", 8)

def generate_room_code():
    '''
    generate a unique room code
    '''
    while True:
        code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(ROOM_CODE_LENGTH))
        if not Room.objects.filter(code=code).exists():
            return code

class Room(models.Model):
    '''
    represents a centralised model for getting data and for processing
    '''
    code = models.CharField(_("room code"), default=generate_room_code, max_length=ROOM_CODE_LENGTH)
    domain = models.CharField(_("domain name"), max_length=40)
    title = models.CharField(_("name of the room"), max_length=30, blank=True, null=True)
    slug = models.SlugField(max_length=250, blank=True)
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        verbose_name=_("create by"),
        on_delete=models.CASCADE, 
        related_name="rooms",
        blank=True, 
        null=True
    )
    public = models.BooleanField(_("room is public"), default=False)
    email_domain = models.CharField(
        max_length=50,
        verbose_name=_("email domain match"),
        help_text="student email domain name must match this domain",
        blank=True,
        null=True
    )
    
    
    class Meta:
        unique_together = ("code", "domain")

    def __str__(self) -> str:
        return "%s/%s" % (self.domain, self.code)

