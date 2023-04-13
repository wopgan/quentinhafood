from django.db import models

# Create your models here.
class Fornecedor(models.Model):
    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        
    nome = models.CharField(max_length=100, verbose_name="Nome do Fornecedor")
    contato = models.CharField(max_length=11, verbose_name="Contato direto com a Empresa")

    def __str__(self):
        return f"{self.nome}, contato {self.contato}"


class Vendedor(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Vendedor")
    contato = models.CharField(max_length=100, verbose_name="Contato direto com o Vendedor")
    representante = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.nome}, contato {self.contato}, representante da empresa {self.representante}"
