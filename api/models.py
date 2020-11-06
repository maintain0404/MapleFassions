# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from tagging.fields import TagField

class Item(models.Model):
    id = models.IntegerField(primary_key=True)
    category = models.SmallIntegerField()
    set_included = models.ForeignKey('Set', models.DO_NOTHING, db_column='set_included', blank=True, null=True)
    tags = TagField(null = True)
    hsi = models.JSONField(blank=True, null=True) 
    name = models.CharField(max_length=25, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'item'


class Set(models.Model):
    name = models.CharField(max_length=25)
    type = models.SmallIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'set'
