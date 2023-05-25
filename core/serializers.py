from rest_framework import serializers
from .models import Cotacao


class CotacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cotacao
        fields = '__all__'
