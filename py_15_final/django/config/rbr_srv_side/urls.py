from django.urls import path
from .views import ServerViewSet, ServerDetailView, ServerAddView, ServerViewSetShort, ServerTotalInfo, ServerTotalinfoView


urlpatterns = [
    path('servers/', ServerViewSet.as_view()),
    path('servers/<int:pk>', ServerDetailView.as_view()),
    path('servers/add', ServerAddView.as_view()),
    path('servers/status', ServerViewSetShort.as_view()),
    path('servers/totalinfo', ServerTotalInfo.as_view()),
    path('servers/totalinfo_status', ServerTotalinfoView.as_view()),
]
