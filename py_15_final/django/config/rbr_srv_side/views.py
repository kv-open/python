from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .serializer import ServerSerializer
from .serializer import ServerSerializerShort
from .serializer import ServerSerializerServerTotalinfo
from .models import Server
from .models import ServerTotalinfo

class ServerViewSet(generics.ListAPIView):

    queryset = Server.objects.all()
    serializer_class = ServerSerializer

class ServerAddView(generics.CreateAPIView):

    queryset = Server.objects.all()
    serializer_class = ServerSerializer

class ServerDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Server.objects.all()
    serializer_class = ServerSerializer

class ServerViewSetShort(generics.ListAPIView):

    queryset = Server.objects.all()
    serializer_class = ServerSerializerShort

class ServerTotalInfo(generics.CreateAPIView):

    queryset = ServerTotalinfo.objects.all()
    serializer_class = ServerSerializerServerTotalinfo


class ServerTotalinfoView(generics.ListAPIView):

    queryset = ServerTotalinfo.objects.all()
    serializer_class = ServerSerializerServerTotalinfo