from rest_framework_mongoengine import serializers as mongoserializers
from .models import Log


class LogsSerializer(mongoserializers.DocumentSerializer):
    class Meta:
        model = Log
        fields = '__all__'
