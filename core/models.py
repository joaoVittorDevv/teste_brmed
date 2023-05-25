from django.db import models


class Cotacao(models.Model):
    moeda = models.CharField(max_length=50)
    data = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.moeda} - {self.data}: {self.valor}"
