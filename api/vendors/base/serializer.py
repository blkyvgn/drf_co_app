from rest_framework import serializers
from api.vendors.mixins.serializer import SerializerHelpers


class BaseSerializer(SerializerHelpers, serializers.Serializer):
	pass

class BaseModelSerializer(SerializerHelpers, serializers.ModelSerializer):
	pass

