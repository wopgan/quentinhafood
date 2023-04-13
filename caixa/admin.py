from django.contrib import admin
from .models import Entrada, TotalEntrada, Saida
from .models import TotalSaida

admin.site.register(Entrada)
admin.site.register(TotalEntrada)
admin.site.register(Saida)
admin.site.register(TotalSaida)
