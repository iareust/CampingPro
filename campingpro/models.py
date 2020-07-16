# from django.db import models
from django.contrib.gis.db import models


# Create your models here.
class BezirkPoly(models.Model):
    id = models.BigIntegerField(primary_key=True)
    geom = models.MultiPolygonField(blank=True, null=True)
    bezirksnum = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bezirk_poly'


class CampingPoints(models.Model):
    id = models.BigIntegerField(primary_key=True)
    geom = models.PointField(dim=3, blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'camping_points'


class CampingDistance(models.Model):
    id = models.BigIntegerField(primary_key=True)
    geom = models.PointField(dim=3, blank=True, null=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    distance_sbb = models.FloatField(blank=True, null=True)
    distance_see = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'camping_distance'


class FluesseLine(models.Model):
    id = models.BigIntegerField(primary_key=True)
    geom = models.MultiLineStringField(blank=True, null=True)
    objectid_g = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    grosserflu = models.CharField(max_length=20, blank=True, null=True)
    biogeo = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fluesse_line'


class SbbPoints(models.Model):
    id = models.BigIntegerField(primary_key=True)
    geom = models.MultiPointField(blank=True, null=True)
    remark = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sbb_points'


class SeenPoly(models.Model):
    id = models.BigIntegerField(primary_key=True)
    geom = models.MultiPolygonField(blank=True, null=True)
    id0 = models.CharField(max_length=32, blank=True, null=True)
    id1 = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seen_poly'
