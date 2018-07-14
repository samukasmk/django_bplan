from django.db import models

tipos_de_valores = (
    ('BRL', 'R$ (Reais)'),
    ('%', '% (Porcento)'),
)


class CustoFixoMensal(models.Model):
    nome = models.CharField(max_length=50)
    valor = models.FloatField()
    tipo = models.CharField(max_length=3, choices=tipos_de_valores, default='BRL')

    def __str__(self):
        return self.nome


class CustoVariavelDoProduto(models.Model):
    nome = models.CharField(max_length=50)
    valor = models.FloatField()
    tipo = models.CharField(max_length=3, choices=tipos_de_valores, default='BRL')
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nome}: {self.valor} {self.tipo}'


class Produto(models.Model):
    nome = models.CharField(max_length=50)
    qtd_produtos_gerados = models.IntegerField()
    valor_de_venda = models.FloatField()

    def __str__(self):
        return self.nome

    @property
    def total_de_custo(self):
        total_de_custo = 0.0
        for custo in CustoVariavelDoProduto.objects.filter(produto_id=self.id):
            if custo.tipo != '%':
                total_de_custo += custo.valor

        return total_de_custo

    @property
    def lucro_bruto(self):
        return float(self.qtd_produtos_gerados) * self.valor_de_venda

    @property
    def lucro_liquido(self):
        return self.lucro_bruto - self.total_de_custo

    @property
    def porcentagem_de_lucro(self):
            return (self.lucro_liquido * 100) / self.total_de_custo



