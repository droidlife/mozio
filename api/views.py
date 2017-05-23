from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import Providers


class ProviderView(APIView):
    def post(self, request):

        if Providers.objects.filter(email=request.data['email'], is_deleted=False).exists():
            response = {
                'result': False,
                'message': 'Sorry provider corresponding to the email already exists.'
            }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            Providers.objects.create(**request.data)

            response = {
                'result': True,
                'message': 'Provider added successfully.'
            }

            return Response(response, status=status.HTTP_200_OK)

    def put(self, request):
        if not Providers.objects.filter(pk=request.data['id']).exists():
            response = {
                'result': False,
                'message': 'Sorry provider does not exists.'
            }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            Providers.objects.filter(pk=request.data['id']).update(**request.data['data'])

            response = {
                'result': True,
                'message': 'Provider updated successfully.'
            }

            return Response(response, status=status.HTTP_200_OK)

    def get(self, request):
        from .serializers import provider_serializers

        response = {
            'result': True,
            'message': 'Providers fetched successfully',
            'data': provider_serializers(Providers.objects.filter(is_deleted=False))
        }

        return Response(response, status=status.HTTP_200_OK)

    def delete(self, request):
        provider_id = int(request.data['id'])

        provider = Providers.objects.filter(pk=provider_id, is_deleted=False).first()

        if provider:
            provider.is_deleted = True
            provider.save()

            response = {
                'result': True,
                'message': 'Provider deleted successfully.'
            }

            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'result': False,
                'message': 'Sorry provider not found.'
            }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class PolygonView(APIView):
    def post(self, request):
        from .service import create_polygon

        provider_id = request.data['provider_id']
        name = request.data['name']
        price = request.data['price']
        coordinates = request.data['coordinate'][0]

        provider = Providers.objects.filter(pk=provider_id, is_deleted=False).first()

        if provider:
            create_polygon(coordinates=coordinates,
                           price=price,
                           provider_id=provider_id,
                           name=name)

            response = {
                'result': True,
                'message': 'Polygon added successfully.'
            }

            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'result': False,
                'message': 'Sorry provider not found.'
            }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        from .models import Polygons
        from .serializers import polygon_serializer

        provider_id = int(request.query_params['provider_id'])

        provider = Providers.objects.filter(pk=provider_id, is_deleted=False).first()

        if provider:
            response = {
                'result': True,
                'message': 'Polygons fetched successfully.',
                'data': polygon_serializer(Polygons.objects.filter(is_deleted=False,
                                                                   providers_id=provider_id))
            }

            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'result': False,
                'message': 'Sorry provider not found.'
            }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        from .models import Polygons
        polygon_id = request.data['polygon_id']

        polygon = Polygons.objects.filter(is_deleted=False, pk=polygon_id).first()

        if polygon:
            polygon.is_deleted = True
            polygon.save()

            response = {
                'result': True,
                'message': 'Polygon deleted successfully.'
            }

            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'result': False,
                'message': 'Sorry polygon not found.'
            }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class GetPolygonFromPointView(APIView):
    def get(self, request):
        from .service import filter_polygons
        latitude = request.query_params['lat']
        longitude = request.query_params['lng']

        response = {
            'result': True,
            'message': 'Polygons fetched successfully.',
            'data': filter_polygons([latitude, longitude])
        }

        return Response(response, status=status.HTTP_200_OK)
