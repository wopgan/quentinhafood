from django.contrib import admin
from .models import Cliente, Debito, Pedido

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Debito)
admin.site.register(Pedido)
