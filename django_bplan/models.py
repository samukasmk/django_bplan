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



class Insumo(models.Model):
    nome = models.CharField(max_length=50)
    valor = models.FloatField()
    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.nome} (R$ {self.valor})'

class CustoVariavelDoProduto(models.Model):
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    insumo = models.OneToOneField(Insumo, on_delete=models.CASCADE)
    porcentagem_de_uso = models.IntegerField(default=100)
    descricao_curta = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.insumo.nome} para {self.produto.nome}'

    @property
    def total_da_fracao(self):
        return (self.insumo.valor * float(self.porcentagem_de_uso)) / 100

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
            total_de_custo += custo.total_da_fracao

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



