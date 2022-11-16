from django.contrib import admin

# Register your models here.
from .models import Room, GenerationSettings, AvalilableOptionChoices, AvailableOption

class OptionsInLine(admin.TabularInline):
    model = AvalilableOptionChoices.options.through

class AvalilableOptionsAdmin(admin.ModelAdmin):
    inlines = [
        OptionsInLine,
    ]
    fields = ("title", "room")

admin.site.register(Room)
admin.site.register(GenerationSettings)
admin.site.register(AvalilableOptionChoices, AvalilableOptionsAdmin)
# unregistered to reduce confusion
# admin.site.register(AvailableOption)