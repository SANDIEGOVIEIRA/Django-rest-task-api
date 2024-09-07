from rest_framework import serializers
from .models import api_restful

class api_Serializer(serializers.ModelSerializer):
    class Meta:
        model = api_restful
        fields = '__all__'
