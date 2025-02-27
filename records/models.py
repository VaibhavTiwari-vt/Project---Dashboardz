from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class RecordsName(models.Model):
    name = models.CharField(unique=True, max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'records_name'
        verbose_name = "Record Name"
        verbose_name_plural = "Records Names"

    def __str__(self):
        return self.name
    

class Field2Names(models.Model):
    name = models.CharField(max_length=45)
    records_name = models.ForeignKey('RecordsName', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'field_2_names'
        unique_together = (('records_name', 'name'),)
        verbose_name = "Field 2 Name"
        verbose_name_plural = "Field 2 Names"
    
    def __str__(self):
        return self.name
    


class FieldNames(models.Model):
    field_1 = models.CharField(max_length=45, blank=True, null=True)
    field_2 = models.CharField(max_length=45, blank=True, null=True)
    field_3 = models.CharField(max_length=45, blank=True, null=True)
    records_name = models.ForeignKey('RecordsName', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'field_names'
        verbose_name = "Field Name"
        verbose_name_plural = "Field Names"


class FieldValues(models.Model):
    field_1 = models.FloatField()
    field_2 = models.ForeignKey(Field2Names, models.DO_NOTHING)
    field_3 = models.DateField(default=timezone.now)
    description = models.TextField()
    owner = models.ForeignKey(User, models.DO_NOTHING, db_column='owner', to_field='username')  # Assuming AuthUser refers to User
    records_name = models.ForeignKey('RecordsName', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'field_values'
        ordering = ['-field_3']
        verbose_name = "Field Value"
        verbose_name_plural = "Field Values"
