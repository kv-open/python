from rest_framework import serializers
from .models import Server
from .models import ServerTotalinfo


class ServerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Server
        fields = ['id', 'ip_address', 'description', 'name', 'server_is_active']

class ServerSerializerShort(serializers.ModelSerializer):

    class Meta:
        model = Server
        fields = ['ip_address', 'server_is_active']

class ServerSerializerServerTotalinfo(serializers.ModelSerializer):

    class Meta:
        model = ServerTotalinfo
        fields = ['totalinfo']
