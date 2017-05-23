def provider_serializers(provider_list):
    response = []

    for provider in provider_list:
        response.append({
            'id': provider.id,
            'name': provider.name,
            'email': provider.email,
            'language': provider.language,
            'currency': provider.currency,
            'is_deleted': provider.is_deleted,
            'phone_number': provider.phone_number
        })

    return response


def polygon_serializer(polygon_list):
    import json
    response = []

    for polygon in polygon_list:
        response.append({
            'id': polygon.id,
            'name': polygon.name,
            'price': polygon.price,
            'geojson': json.loads(polygon.geopoints.geojson)
        })

    return response
