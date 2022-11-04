from django.contrib import admin

# Register your models here.
from .models import Room, GenerationSettings, AvalilableOptionChoices, AvailableOption

class OptionsInLine(admin.TabularInline):
    model = AvalilableOptionChoices.options.through

class AvalilableOptionsAdmin(admin.ModelAdmin):

    fields = ("title","room", "options")

admin.site.register(Room)
admin.site.register(GenerationSettings)
admin.site.register(AvalilableOptionChoices)
admin.site.register(AvailableOption)