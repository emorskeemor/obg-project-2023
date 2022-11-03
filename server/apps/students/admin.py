from django.contrib import admin

# Register your models here.
from .models import Student, Option, Choice, Requirement

class OptionsInLine(admin.TabularInline):
    model = Student.options.through

class StudentAdmin(admin.ModelAdmin):
    inlines = [
        OptionsInLine,
    ]

admin.site.register(Student, StudentAdmin)
admin.site.register(Option)
admin.site.register(Choice)
admin.site.register(Requirement)
