from django.db import models
from django.db.models.signals import post_save
from datetime import date
from django.dispatch import receiver

class Cliente(models.Model):
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    nome = models.CharField(max_length=100, verbose_name="Nome do cliente")
    telefone = models.CharField(max_length=11, verbose_name="Telefone para Contato")
    endereco = models.TextField(verbose_name="Endereço do cliente")
    referencia = models.TextField(verbose_name="Ponto de Referencia")

    def __str__(self):
        return self.nome


class Debito(models.Model):
    debito = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Debitos do Cliente")
    data = models.DateField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CharField)

    def __str__(self):
        return f"{self.cliente}, esta com o saldo negativo de {self.debito}, na data {self.data}"


class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    qnt_marmita = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Quantidade de Marmitas")
    valor_marmita = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor da Marmita")
    total_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True, verbose_name="Total do pedido")
    data = models.DateField(default=date.today)
    descricao = models.TextField()
    is_pago = models.BooleanField(default=False, verbose_name="Pedido Pago?")
    is_entregue = models.BooleanField(default=False, verbose_name="Pedido Entregue")

    def calcular_total_pedido(self):
        self.total_pedido = self.qnt_marmita * self.valor_marmita

    def atualizar_debito(self):
        if not self.is_pago:
            debito, created = Debito.objects.get_or_create(cliente=self.cliente)
            debito.debito += self.total_pedido
            debito.save()

    def save(self, *args, **kwargs):
        self.calcular_total_pedido()
        super(Pedido, self).save(*args, **kwargs)
        self.atualizar_debito()

    def update_debito(self, old_pedido):
        if self.is_pago and not old_pedido.is_pago:
            debito = Debito.objects.get(cliente=self.cliente)
            debito.debito -= old_pedido.total_pedido
            debito.debito += self.total_pedido
            debito.save()

    def __str__(self):
        if self.is_pago == True and self.is_entregue == True:
            return f"Pedido numero {self.id} do cliente {self.cliente}, pago e já saiu pra entraga"

        if self.is_pago == True:
            return f"Pedido numero {self.id} para o cliente {self.cliente} são {self.qnt_marmita} marmitas, pago e aguardando entrega."
        
        if self.is_entregue == True:
            return f"Pedido numero {self.id} do cliente {self.cliente} saiu para entrega"

        
        return f"Pedido numero {self.id} do cliente, {self.cliente}, foi {self.qnt_marmita} marmitas e esta aguardando entrega - valor RS {self.total_pedido} a receber "

@receiver(post_save, sender=Pedido)
def update_debito(sender, instance, **kwargs):
    if instance.is_pago:
        # Se o pedido está pago, atualize o valor do débito do cliente
        debito = Debito.objects.get(cliente=instance.cliente)
        total_pedido = instance.total_pedido
        debito.debito -= total_pedido
        debito.save()
    else:
        # Se o pedido não está pago, não é necessário atualizar o débito do cliente
        pass



