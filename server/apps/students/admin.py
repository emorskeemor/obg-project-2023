from django.contrib import admin

# Register your models here.
from .models import Student, Option, Choice

admin.site.register(Student)
admin.site.register(Option)
admin.site.register(Choice)