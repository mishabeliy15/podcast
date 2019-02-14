from .models import Record
from rest_framework import serializers


class RecordSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Record
        fields = '__all__'
