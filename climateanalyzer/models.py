from django.db import models

# Create your models here.
class Belongsto(models.Model):
    city = models.CharField(max_length=26, blank=True, null=True)
    state = models.CharField(max_length=26, blank=True, null=True)
    id = models.BigIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'belongsto'


class City(models.Model):
    dt = models.DateField(blank=True, null=True)
    averagetemperature = models.DecimalField(max_digits=38, decimal_places=17, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)
    id = models.BigIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'city'


class Consistsof(models.Model):
    state = models.CharField(max_length=26, blank=True, null=True)
    country = models.CharField(max_length=26, blank=True, null=True)
    id = models.BigIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'consistsof'


class Country(models.Model):
    dt = models.DateField(blank=True, null=True)
    averagetemperature = models.DecimalField(max_digits=38, decimal_places=17, blank=True, null=True)
    country = models.CharField(max_length=26, blank=True, null=True)
    id = models.BigIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'country'


class Django(models.Model):
    id = models.FloatField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django'

class President(models.Model):
    president_name = models.CharField(max_length=128, blank=True, null=True)
    term_start = models.DateField(blank=True, null=True)
    term_end = models.DateField(blank=True, null=True)
    party = models.CharField(max_length=26, blank=True, null=True)
    id = models.BigIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'president'

class State(models.Model):
    dt = models.DateField(blank=True, null=True)
    averagetemperature = models.DecimalField(max_digits=38, decimal_places=15, blank=True, null=True)
    state = models.CharField(max_length=26, blank=True, null=True)
    country = models.CharField(max_length=26, blank=True, null=True)
    id = models.BigIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'state'