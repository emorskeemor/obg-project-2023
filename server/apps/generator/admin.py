from django.contrib import admin

# Register your models here.
from .models import InsertTogether, Block, OptionBlocks

admin.site.register(InsertTogether)
admin.site.register(Block)
admin.site.register(OptionBlocks)