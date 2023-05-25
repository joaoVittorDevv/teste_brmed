from rest_framework import viewsets
from .models import Cotacao
from .serializers import CotacaoSerializer


class CotacaoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cotacao.objects.all()
    serializer_class = CotacaoSerializer

