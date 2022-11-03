from django.contrib import admin

# Register your models here.
from .models import InsertTogether, Block, OptionBlocks

class OptionsInLine(admin.TabularInline):
    model = Block.options.through

class BlockAdmin(admin.ModelAdmin):
    inlines = [
        OptionsInLine,
    ]


admin.site.register(InsertTogether)
admin.site.register(Block, BlockAdmin)
admin.site.register(OptionBlocks)