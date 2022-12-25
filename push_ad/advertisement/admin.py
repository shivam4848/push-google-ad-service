from django.contrib import admin

from advertisement.models import BQExampleData


# Register your models here.
@admin.register(BQExampleData)
class BQExampleDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'phone_number']
