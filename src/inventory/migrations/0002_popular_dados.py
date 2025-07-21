import random

from django.db import migrations

SUPPLIER_KEYWORDS = {
    'The Coca-Cola Company': ['Coca-Cola', 'Fanta', 'Sprite', 'Del Valle', 'Schweppes'],
    'Ambev': ['Guaraná Antarctica', 'Pepsi', 'H2O', 'Brahma', 'Skol', 'Stella Artois'],
    'Heineken Brasil': ['Heineken', 'Corona'],
    'Nestlé': ['Nescafé', 'Moça', 'Vono'],
    'Pepsico': ['Elma Chips', 'Doritos'],
    'Mondelez': ['Lacta', 'Oreo'],
    'Outros': ['Vero', 'Strike', 'Santa Clara', 'Maped', 'Vitasuco', 'Grapette', 'Gallo', 'Heinz']
}

def get_supplier_name(product_name: str) -> str:
    """
    Determina o nome do fornecedor com base em palavras-chave no nome do produto.
    Esta é a função correta que substitui a versão com @task.
    """
    for supplier, keywords in SUPPLIER_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in product_name.lower():
                return supplier
    return 'Distribuidor Geral'

def popular_banco(apps, schema_editor):
    """
    Função principal que popula o banco de dados com produtos e fornecedores.
    """
    Product = apps.get_model('inventory', 'Product')
    Supplier = apps.get_model('inventory', 'Supplier')
    ProductSupplier = apps.get_model('inventory', 'ProductSupplier')

    products_data = [
        {"name": "Coca-Cola Original 350ml", "description": "Lata de 350ml do clássico refrigerante de cola."},
        {"name": "Coca-Cola Zero 2L", "description": "Garrafa de 2 litros, sem açúcar."},
        {"name": "Guaraná Antarctica 350ml", "description": "Lata do autêntico guaraná do Brasil."},
        {"name": "Guaraná Antarctica Zero 1L", "description": "Garrafa de 1 litro, sem açúcar."},
        {"name": "Pepsi Black 2L", "description": "Garrafa de 2 litros, máximo sabor sem açúcar."},
        {"name": "Fanta Laranja 600ml", "description": "Garrafa de 600ml com sabor refrescante de laranja."},
        {"name": "Fanta Uva 350ml", "description": "Lata com o delicioso sabor de uva."},
        {"name": "Sprite Original 500ml", "description": "Sabor de limão refrescante."},
        {"name": "H2OH! Limoneto 500ml", "description": "Bebida levemente gaseificada com um toque de limão."},
        {"name": "Schweppes Tônica 350ml", "description": "Lata de água tônica, ideal para drinks."},

        {"name": "Cerveja Heineken Long Neck 330ml", "description": "Produto para maiores de 18 anos. Cerveja premium."},
        {"name": "Cerveja Heineken Zero Álcool 350ml", "description": "Produto para maiores de 18 anos. O sabor de Heineken, sem álcool."},
        {"name": "Cerveja Stella Artois Long Neck 275ml", "description": "Produto para maiores de 18 anos. Sofisticação e sabor único."},
        {"name": "Cerveja Brahma Duplo Malte 350ml", "description": "Produto para maiores de 18 anos. A combinação de malte pilsner e munique."},
        {"name": "Cerveja Skol Pilsen 473ml (Latão)", "description": "Produto para maiores de 18 anos. A cerveja que desce redondo."},
        {"name": "Cerveja Corona Extra 355ml", "description": "Produto para maiores de 18 anos. Perfeita com uma fatia de limão."},
        {"name": "Cerveja Brahma Chopp 1L (Retornável)", "description": "Produto para maiores de 18 anos. Cremosidade e sabor em tamanho família."},

        {"name": "Suco Del Valle Uva 1L", "description": "Néctar de uva em embalagem de 1 litro."},
        {"name": "Suco Del Valle Laranja 1L", "description": "Néctar de laranja, fonte de vitamina C."},
        {"name": "Água Tônica Schweppes Citrus 350ml", "description": "Mix de sabores cítricos com a clássica tônica."},

        {"name": "Batata Frita Elma Chips Sensações 80g", "description": "Sabor peito de peru com toque de azeite."},
        {"name": "Salgadinho Doritos Queijo Nacho 140g", "description": "O clássico salgadinho de milho com queijo."},
        {"name": "Chocolate Lacta ao Leite 90g", "description": "Barra de chocolate ao leite cremoso."},
        {"name": "Biscoito Oreo Original 90g", "description": "O famoso biscoito de chocolate com recheio de baunilha."},
        {"name": "Amendoim Japonês Elma Chips 150g", "description": "Amendoim crocante com casquinha de soja e shoyu."},
        {"name": "Sopa Vono de Queijo com Tomate e Manjericão", "description": "Sopa instantânea prática e saborosa."},
        {"name": "Leite Condensado Moça 395g", "description": "Leite condensado integral, perfeito para sobremesas."},
        {"name": "Café Solúvel Nescafé Original 100g", "description": "Café solúvel para um preparo rápido e prático."},
        {"name": "Azeite de Oliva Extra Virgem Gallo 500ml", "description": "Azeite português de alta qualidade."},
        {"name": "Molho de Tomate Tradicional Heinz 300g", "description": "Molho de tomate pronto para suas receitas."}
    ]

    supplier_names = set(get_supplier_name(p['name']) for p in products_data)
    suppliers_to_create = [Supplier(name=name) for name in supplier_names]
    Supplier.objects.bulk_create(suppliers_to_create, ignore_conflicts=True)

    suppliers = {s.name: s for s in Supplier.objects.all()}

    for item in products_data:
        price = round(random.uniform(3.50, 25.00), 2)

        product, created = Product.objects.get_or_create(
            name=item['name'],
            defaults={
                'description': item.get('description', '') or 'Sem descrição',
                'price': price
            }
        )

        if created:
            supplier_name = get_supplier_name(product.name)
            supplier_obj = suppliers.get(supplier_name)

            if supplier_obj:
                ProductSupplier.objects.create(
                    product=product,
                    supplier=supplier_obj
                )

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(popular_banco),
    ]
