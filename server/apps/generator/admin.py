from django.contrib import admin

# Register your models here.
from .models import InsertTogether, Block, OptionBlocks, BlockSubject



class OptionsInLine(admin.TabularInline):
    model = Block.options.through

class BlockAdmin(admin.ModelAdmin):
    inlines = [
        OptionsInLine,
    ]
    fields = ("number_of_subjects", "block_id", "blocks")


admin.site.register(InsertTogether)
admin.site.register(Block, BlockAdmin)
admin.site.register(OptionBlocks)
admin.site.register(BlockSubject)