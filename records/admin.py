from django.contrib import admin
from .models import RecordsName, FieldNames, Field2Names, FieldValues


# Register Models in Django Admin
@admin.register(RecordsName)
class RecordsNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Customize columns in the admin panel
    search_fields = ('name',)


@admin.register(FieldNames)
class FieldNamesAdmin(admin.ModelAdmin):
    list_display = ('id', 'field_1', 'field_2', 'field_3', 'records_name')
    search_fields = ('field_1', 'field_2', 'field_3')


@admin.register(Field2Names)
class Field2NamesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'records_name')
    search_fields = ('name',)


@admin.register(FieldValues)
class FieldValuesAdmin(admin.ModelAdmin):
    list_display = ('id', 'field_1', 'field_2', 'field_3', 'description', 'owner', 'records_name')
    search_fields = ('description',)
    list_filter = ('field_3', 'owner')  # Adds filtering options in admin panel
