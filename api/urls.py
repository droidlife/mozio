from django.conf.urls import url
from .views import ProviderView, PolygonView, GetPolygonFromPointView

urlpatterns = [
    url(r'^providers', ProviderView.as_view()),
    url(r'^polygon', PolygonView.as_view()),
    url(r'^get/polygon/from/points', GetPolygonFromPointView.as_view())
]
