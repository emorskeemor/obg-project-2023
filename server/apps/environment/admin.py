from django.contrib import admin

# Register your models here.
from .models import Room, GenerationSettings, AvalilableOptions, AvailableOption

# class OptionsInLine(admin.TabularInline):
#     model = AvalilableOptions.options.through

# class AvalilableOptionsAdmin(admin.ModelAdmin):
#     inlines = [
#         OptionsInLine,
#     ]
#     fields = ("title","room", "options")

admin.site.register(Room)
admin.site.register(GenerationSettings)
admin.site.register(AvalilableOptions)
admin.site.register(AvailableOption)