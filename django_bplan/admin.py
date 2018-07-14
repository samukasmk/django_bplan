from django.contrib import admin
from .models import CustoFixoMensal, CustoVariavelDoProduto, Produto, Insumo


@admin.register(CustoFixoMensal)
class CustoFixoMensalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor', 'tipo')


@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor', 'descricao')


class CustoVariavelDoProdutoInline(admin.TabularInline):
    model = CustoVariavelDoProduto
    extra = 1


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 'total_de_custo', 'qtd_produtos_gerados', 'valor_de_venda', 'lucro_bruto', 'lucro_liquido',
        'porcentagem_de_lucro')

    # filter_horizontal = ('custos_variaveis',)

    inlines = [
        CustoVariavelDoProdutoInline,
    ]
