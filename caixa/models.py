from django.db import models
from django.db.models.signals import post_save
from datetime import date
from django.dispatch import receiver
from cliente.models import Pedido

class Entrada(models.Model):
    entrada = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor entrada")
    data = models.DateField(auto_now_add=True)
    razao = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total de entradas associadas ao pedido")

    def __str__(self):
        return(
            f"Entrada de {self.razao.total_pedido} referente ao pedido numero {self.razao.id} "
            f"Entrada dia {self.data}"
        )

class TotalEntrada(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total de entradas")
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Total de entradas até o presente dia {self.data} é de R${self.total} "


class Saida(models.Model):
    saida = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor Saida")
    data = models.DateField(auto_now_add=True)
    descricao = models.TextField(verbose_name="Descrição da saida")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total de Saidas")

    def __str__(self):
        return f"Total de saidas até o momento é de {self.saida}"

    def save(self, *args, **kwargs):
        total_saidas, _ = TotalSaida.objects.get_or_create()
        total_saidas.total += self.saida
        total_saidas.save()
        super().save(*args, **kwargs)


class TotalSaida(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total de entradas")
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Total de saida até o presente dia {self.data} é de R$ {self.total} "


@receiver(post_save, sender=Pedido)
def criar_entrada(sender, instance, created, **kwargs):
    if instance.is_pago and created:  # Verifica se o Pedido foi criado e está pago
        entrada = Entrada(entrada=instance.total_pedido, razao=instance)
        entrada.save()
        total_entradas = Entrada.objects.filter(razao=instance).aggregate(models.Sum('entrada'))['entrada__sum']
        instance.entrada_set.update(total=total_entradas or 0)

        total_entrada_diaria, created = TotalEntrada.objects.get_or_create(data=date.today())
        total_entrada_diaria.total += instance.total_pedido
        total_entrada_diaria.save()
