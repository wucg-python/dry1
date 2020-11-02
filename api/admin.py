from django.contrib import admin

# Register your models here.
from api import models

admin.site.register(models.Publisher)
admin.site.register(models.Book)
admin.site.register(models.Author)