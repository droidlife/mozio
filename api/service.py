from .models import Polygons


def create_polygon(coordinates, provider_id, name, price):
    coordinate_string_array = []
    for coordinate in coordinates:
        coordinate_string_array.append(str(coordinate[0]) + ' ' + str(coordinate[1]))

    coordinate_string = 'POLYGON((' + ','.join(coordinate_string_array) + '))'

    polygon = Polygons(geopoints=coordinate_string, providers_id=provider_id,
                       name=name, price=price)
    polygon.save()


def filter_polygons(points):
    from django.contrib.gis.geos import GEOSGeometry
    import json
    response = []

    point_string = 'POINT(' + str(points[0]) + ' ' + str(points[1]) + ')'
    coordinate = GEOSGeometry(point_string)

    for polygon in Polygons.objects.filter(geopoints__intersects=coordinate):
        response.append({
            'id': polygon.id,
            'name': polygon.name,
            'price': polygon.price,
            'geojson': json.loads(polygon.geopoints.geojson)
        })

    return response
