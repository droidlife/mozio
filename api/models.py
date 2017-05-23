from __future__ import unicode_literals

from django.contrib.gis.db import models


class Polygons(models.Model):
    providers = models.ForeignKey('Providers')
    geopoints = models.GeometryField()
    name = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    is_deleted = models.NullBooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'polygons'


class Providers(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    currency = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_deleted = models.NullBooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'providers'
