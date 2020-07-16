from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.template import RequestContext
from datetime import datetime
from django.core.serializers import serialize
from django.db import connection

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.gis.measure import Distance

from campingpro.models import *
from django.template.context import Context
import pandas as pd
import psycopg2

from django.contrib.gis.geos import GEOSGeometry


# Create your views here.

def seen_dataset(request):
    query = """
    with results as (
    select
    	sp.id,
    	sp.geom,
    	sp.id1,
    	count(sp.id) as num_bordering_regions
    from
    	seen_poly sp
    join bezirk_poly bp on
    	ST_Touches(sp.geom,
    	bp.geom)
    group by
    	sp.id )
    select
    	json_build_object( 'type', 'FeatureCollection', 'features', json_agg(st_asgeojson(results)::json))
    from
    	results
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        queryset = cursor.fetchall()[0][0]
        return JsonResponse(queryset)


def camping_dataset(request):
    seen = serialize('geojson', CampingPoints.objects.all())
    return HttpResponse(seen, content_type='json')


def borders_dataset(request):
    query = """
    SELECT json_build_object(
        	'type', 'FeatureCollection',
        	'features', json_agg(ST_AsGeoJSON(bcp.*)::json)
        	)
    FROM (
    	SELECT bp.*, (count(cp.geom)/ST_Area(bp.geom::geography)) AS num_camping
    	FROM bezirk_poly as bp LEFT JOIN camping_points as cp
    	ON st_contains(bp.geom,cp.geom) 
    	GROUP BY bp.id
    ) bcp;
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        queryset = cursor.fetchall()[0][0]
        return JsonResponse(queryset)

    # borders = serialize('geojson', BezirkPoly.objects.all())
    # return HttpResponse(borders, content_type='json')


def get_ninecut_intint(request):
    poly_a = request.GET.get('polyA', None)
    poly_b = request.GET.get('polyB', None)

    query = """
    select
	    json_build_object( 'type', 'FeatureCollection', 'features', json_agg(st_asgeojson(ST_Intersection(st_setsrid(st_astext(st_geomfromgeojson('{}')), 4326), st_setsrid(st_astext(st_geomfromgeojson('{}')), 4326)))::json))
    """.format(poly_a, poly_b)

    return JsonResponse(__helper_get_ninecut(query))


def get_ninecut_intbound(request):
    poly_a = request.GET.get('polyA', None)
    poly_b = request.GET.get('polyB', None)

    query = """
    select
	    json_build_object( 'type', 'FeatureCollection', 'features', json_agg(st_asgeojson(
	    ST_Intersection(st_setsrid(st_astext(st_geomfromgeojson('{}')), 4326), ST_Boundary(st_setsrid(st_astext(st_geomfromgeojson('{}')), 4326))))::json
	    ))
    """.format(poly_a, poly_b)

    return JsonResponse(__helper_get_ninecut(query))


def get_ninecut_intext(request):
    poly_a = request.GET.get('polyA', None)
    poly_b = request.GET.get('polyB', None)

    query = """
    select
	    json_build_object( 'type', 'FeatureCollection', 'features', json_agg(st_asgeojson(
	    ST_Difference(st_setsrid(st_astext(st_geomfromgeojson('{}')), 4326), st_setsrid(st_astext(st_geomfromgeojson('{}')), 4326)))::json
	    ))
    """.format(poly_a, poly_b)

    return JsonResponse(__helper_get_ninecut(query))


def get_ninecut_boundint(request):
    poly_a = request.GET.get('polyA', None)
    poly_b = request.GET.get('polyB', None)

    query = """
    select
	    json_build_object( 'type', 'FeatureCollection', 'features', json_agg(st_asgeojson(
	    ST_Intersection(ST_Boundary(st_setsrid(st_astext(st_geomfromgeojson('{}')), 4326)), st_setsrid(st_astext(st_geomfromgeojson('{}')), 4326)))::json
	    ))
    """.format(poly_a, poly_b)

    return JsonResponse(__helper_get_ninecut(query))


def get_ninecut_boundbound(request):
    poly_a = request.GET.get('polyA', None)
    poly_b = request.GET.get('polyB', None)

    query = """
    select
	    json_build_object( 'type', 'FeatureCollection', 'features', json_agg(st_asgeojson(
	    ST_Intersection(ST_Boundary(st_setsrid(st_astext(st_geomfromgeojson('{}')), 4326)), ST_Boundary(st_setsrid(st_astext(st_geomfromgeojson('{}')), 4326))))::json
	    ))
    """.format(poly_a, poly_b)

    return JsonResponse(__helper_get_ninecut(query))


def get_ninecut_boundext(request):
    poly_a = request.GET.get('polyA', None)
    poly_b = request.GET.get('polyB', None)

    query = """
    select
	    json_build_object( 'type', 'FeatureCollection', 'features', json_agg(st_asgeojson(
	    ST_Difference(ST_Boundary(st_setsrid(st_astext(st_geomfromgeojson('{}')), 4326)), st_setsrid(st_astext(st_geomfromgeojson('{}')), 4326)))::json
	    ))
    """.format(poly_a, poly_b)

    return JsonResponse(__helper_get_ninecut(query))


def get_ninecut_extint(request):
    poly_a = request.GET.get('polyA', None)
    poly_b = request.GET.get('polyB', None)

    query = """
    select
	    json_build_object( 'type', 'FeatureCollection', 'features', json_agg(st_asgeojson(
	    ST_Difference(st_setsrid(st_astext(st_geomfromgeojson('{}')), 4326), st_setsrid(st_astext(st_geomfromgeojson('{}')), 4326)))::json
	    ))
    """.format(poly_b, poly_a)

    return JsonResponse(__helper_get_ninecut(query))


def get_ninecut_extbound(request):
    poly_a = request.GET.get('polyA', None)
    poly_b = request.GET.get('polyB', None)

    query = """
    select
	    json_build_object( 'type', 'FeatureCollection', 'features', json_agg(st_asgeojson(
	    ST_Difference(ST_Boundary(st_setsrid(st_astext(st_geomfromgeojson('{}')), 4326)), st_setsrid(st_astext(st_geomfromgeojson('{}')), 4326)))::json
	    ))
    """.format(poly_b, poly_a)

    return JsonResponse(__helper_get_ninecut(query))


def get_ninecut_extext(request):
    poly_a = request.GET.get('polyA', None)
    poly_b = request.GET.get('polyB', None)

    query = """
    with sp as (
    select
    	ST_Union(bp.geom) as geom
    from
    	bezirk_poly as bp )
    select
    	json_build_object( 'type', 'FeatureCollection', 'features', json_agg(st_asgeojson(ST_Difference(sp.geom,pp))::json))
    from
    	sp,
    	ST_Union(st_setsrid(st_astext(st_geomfromgeojson('{}')),
    	4326),
    	st_setsrid(st_astext(st_geomfromgeojson('{}')),
    	4326)) as pp
    """.format(poly_b, poly_a)

    return JsonResponse(__helper_get_ninecut(query))


def __helper_get_ninecut(query):
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            queryset = cursor.fetchall()[0][0]
            return queryset

        except:
            print("Invalid SQL Query. Probably self-overlapping Polygon")

        return {}


def get_ninecut_matrix(request):
    poly_a = request.GET.get('polyA', None)
    poly_b = request.GET.get('polyB', None)

    query = """
    select
    	ST_Relate(
    	    st_setsrid(st_astext(st_geomfromgeojson('{}')),	4326),
    	    st_setsrid(st_astext(st_geomfromgeojson('{}')), 4326)
    	)
    """.format(poly_a, poly_b)

    with connection.cursor() as cursor:
        cursor.execute(query)
        queryset = cursor.fetchall()[0][0]
        data = {'int_int': queryset[0],
                'int_bound': queryset[1],
                'int_ext': queryset[2],
                'bound_int': queryset[3],
                'bound_bound': queryset[4],
                'bound_ext': queryset[5],
                'ext_int': queryset[6],
                'ext_bound': queryset[7],
                'ext_ext': queryset[8]}
        return JsonResponse(data)


def get_region_ninecut(request):
    position = [request.GET.get('mouse_position_lat', None), request.GET.get('mouse_position_lng', None)]
    point = 'SRID={};POINT({} {})'.format(4326, position[1], position[0])
    query = """
    select
	    json_build_object( 'type', 'FeatureCollection', 'features', json_agg(st_asgeojson(cc.*)::json) )
    from
    	( with closest_candidates as (
    	select
    		bp.geom
    	from
    		bezirk_poly as bp
    	order by
    		bp.geom <-> '{0}'::geometry
    	limit 5 )
    	select
    		cc.geom
    	from
    		closest_candidates as cc
    	order by
    		ST_Distance( geom,
    		'{0}'::geometry )
    	limit 1 ) cc;
    """.format(point)

    with connection.cursor() as cursor:
        cursor.execute(query)
        queryset = cursor.fetchall()[0][0]
        return JsonResponse(queryset)


def get_nearest_sbb_station(request):
    position = [request.GET.get('mouse_position_lat', None), request.GET.get('mouse_position_lng', None)]
    point = 'SRID={};POINT({} {})'.format(4326, position[1], position[0])
    query = """
    SELECT json_build_object(
    	'type', 'FeatureCollection',
    	'features', json_agg(ST_AsGeoJSON(cc.*)::json)
    	)
    FROM (
    	WITH closest_candidates AS (
    		SELECT sp.id, sp.geom, sp."Name" as name
    		FROM sbb_points_2 AS sp
    		WHERE sp."Verkehrsmittel" like '%Zug%'
    		ORDER BY
    			sp.geom <-> 
    			'{}'::geometry
    		LIMIT 5
    	)
    	SELECT *
    	FROM closest_candidates
    	ORDER BY
    		ST_Distance(
    		geom,
    		'{}'::geometry	
    		)
    	LIMIT 1
    ) cc;
    """.format(point, point)

    with connection.cursor() as cursor:
        cursor.execute(query)
        queryset = cursor.fetchall()[0][0]
        return JsonResponse(queryset)


def camping_dataset2(request):
    distance_lake = request.GET.get('distance_from_water', None)
    distance_sbb = request.GET.get('distance_from_station', None)

    query = """
    SELECT json_build_object(
    	'type', 'FeatureCollection',
    	'features', json_agg(ST_AsGeoJSON(css.*)::json)
    )
    from (
        select cp.id, cp.geom, cp.name, closest_sbb.distance_sbb, closest_lake.distance_lake
        FROM camping_points cp
        CROSS JOIN LATERAL (
            select id, ST_Distance(cp.geom::geography, water.geom::geography) as distance_lake
            FROM (
				select
					sp.geom
				from
					seen_poly sp
					union
				SELECT ST_UnaryUnion(unnest(ST_ClusterWithin(geom, 0.0001))) AS geom FROM fluesse_line
				 ) water
            ORDER BY cp.geom <-> water.geom
            LIMIT 1
        ) AS closest_lake
        CROSS JOIN LATERAL (
            select id, ST_Distance(cp.geom::geography, sp2.geom::geography) as distance_sbb
            FROM (
                SELECT sp.id, sp.geom
                FROM sbb_points_2 AS sp
    		    WHERE sp."Verkehrsmittel" like '%Zug%'
            ) sp2
            ORDER BY cp.geom <-> sp2.geom
            LIMIT 1
        ) AS closest_sbb
        where closest_sbb.distance_sbb <= {} and closest_lake.distance_lake <= {}
    ) css;
    """.format(int(distance_sbb), int(distance_lake) * 1000)

    with connection.cursor() as cursor:
        cursor.execute(query)
        queryset = cursor.fetchall()[0][0]
        return JsonResponse(queryset)


def sbb_water_dataset(request):
    distance_water = request.GET.get('distance_from_water', None)

    query = """
    SELECT json_build_object(
    	'type', 'FeatureCollection',
    	'features', json_agg(ST_AsGeoJSON(css.*)::json)
    )
    from (
        select sp2.id, sp2.geom, sp2."Verkehrsmittel" as type ,sp2."Name" as remark
        FROM (
        	select *
        	from sbb_points_2 sp
        ) sp2
        CROSS JOIN LATERAL (
            select id, ST_Distance(sp2.geom_ch, water.geom) as distance_water
            FROM (
				select
					sp.geom
				from
					seen_poly_ch sp
					union
				SELECT ST_UnaryUnion(unnest(ST_ClusterWithin(geom, 0.0001))) AS geom FROM fluesse_line_ch
				 ) water
            ORDER BY sp2.geom_ch <-> water.geom
            LIMIT 1
        ) AS closest_water
        where closest_water.distance_water <= {}
    ) css;
    """.format(int(distance_water) * 1000)

    with connection.cursor() as cursor:
        cursor.execute(query)
        queryset = cursor.fetchall()[0][0]
        return JsonResponse(queryset)


def routing(request):
    p1 = [request.GET.get('p1_lat', None), request.GET.get('p1_lng', None)]
    p2 = [request.GET.get('p2_lat', None), request.GET.get('p2_lng', None)]

    point1 = 'SRID={};POINT({} {})'.format(4326, p1[1], p1[0])
    point2 = 'SRID={};POINT({} {})'.format(4326, p2[1], p2[0])

    query = """
    SELECT json_build_object(
    	'type', 'FeatureCollection',
    	'features', json_agg(ST_AsGeoJSON(css.*)::json)
    )
    from (
        select edge, st_transform(geom, 4326) from pgr_dijkstra('SELECT id, source, target, "SHAPE_Length" as cost FROM train_network', 
	(SELECT id
	FROM train_network_vertices_pgr tn
	ORDER by tn.the_geom <-> st_transform('{}', 2056)
	LIMIT 1), 
	(SELECT id
	FROM train_network_vertices_pgr tn
	ORDER by tn.the_geom <-> st_transform('{}', 2056)
	LIMIT 1), false) d 
    inner join train_network tn on d.edge = tn.id
    ) css;
    """.format(point1, point2)

    with connection.cursor() as cursor:
        cursor.execute(query)
        queryset = cursor.fetchall()[0][0]
        return JsonResponse(queryset)


def sbb_dataset(request):
    seen = serialize('geojson', SbbPoints.objects.all())
    return HttpResponse(seen, content_type='json')


class SBBStationData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        data = {
            'User': '1'
        }
        return Response(data)


def river_dataset(request):
    river1 = serialize('geojson', FluesseLine.objects.all())
    return HttpResponse(river1, content_type='json')


def ninecut_map(request):
    return render(
        request,
        'app/9cut.html',
        {
            'title': '9-Cut'
        }
    )


def home(request):
    """ Renders home page """
    return render(
        request,
        'app/index.html',
        {
            'title': 'CampingPro',
        }
    )
