from django.contrib import admin
from django.contrib.gis.geos import Point
from datetime import datetime
from leaflet.admin import LeafletGeoAdmin
import pandas as pd

from campingpro.models import BezirkPoly, SbbPoints, SeenPoly, FluesseLine, CampingPoints


class BezirkPolyAdmin(LeafletGeoAdmin):
    pass


class SbbPointsAdmin(LeafletGeoAdmin):
    pass


class SeenPolyAdmin(LeafletGeoAdmin):
    pass


class FluesseLineAdmin(LeafletGeoAdmin):
    pass


class CampingPointsAdmin(LeafletGeoAdmin):
    pass


admin.site.register(BezirkPoly, BezirkPolyAdmin)
admin.site.register(SbbPoints, SbbPointsAdmin)
admin.site.register(SeenPoly, SeenPolyAdmin)
admin.site.register(FluesseLine, FluesseLineAdmin)
admin.site.register(CampingPoints, CampingPointsAdmin)


# Register your models here.
