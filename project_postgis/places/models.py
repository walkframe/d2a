# coding: utf-8
from django.contrib.gis.db import models

SRID = 4326


class Lake(models.Model):
    name = models.CharField(max_length=100)
    geom = models.PolygonField(srid=SRID)

    class Meta:
        db_table = 'lakes'

    def __str__(self):
        return self.name


class Address(models.Model):
    detail = models.CharField(max_length=255)
    geom = models.PointField(srid=SRID)

    class Meta:
        db_table = 'addresses'

    def __str__(self):
        return self.detail
