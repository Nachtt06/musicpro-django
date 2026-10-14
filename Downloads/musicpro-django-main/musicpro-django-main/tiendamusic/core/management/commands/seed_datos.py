from django.core.management.base import BaseCommand
from faker import Faker
from core.models import Rol, UsuarioSistema, Categoria, Proveedor, Producto, Cliente

class Command(BaseCommand):
    help = 'Genera datos masivos configurables usando Faker para MusicPro'

    def add_arguments(self, parser):
        # Permite pasar un argumento --cantidad desde la terminal (ej: python manage.py seed_datos --cantidad 1000)
        parser.add_argument(
            '--cantidad',
            type=int,
            default=20,
            help='Número de productos a generar'
        )

    def handle(self, *args, **options):
        cantidad = options['cantidad']
        fake = Faker('es_CL')
        Faker.seed(42)

        self.stdout.write(self.style.WARNING(f'Iniciando carga masiva de {cantidad} registros...'))

        # 1. Asegurar Roles base
        roles_nombres = ['Administrador', 'Vendedor', 'Bodeguero']
        for r_nombre in roles_nombres:
            Rol.objects.get_or_create(nombre=r_nombre)

        # 2. Asegurar Categorías
        categorias_nombres = ['Cuerdas', 'Percusión', 'Teclados', 'Viento', 'Audio e Iluminación']
        for cat_nombre in categorias_nombres:
            Categoria.objects.get_or_create(nombre=cat_nombre, defaults={'descripcion': fake.sentence()})

        # 3. Asegurar Proveedores (creamos unos 10 si no hay)
        for _ in range(10):
            Proveedor.objects.get_or_create(
                razon_social=fake.company(),
                defaults={
                    'telefono': fake.phone_number(),
                    'email': fake.company_email()
                }
            )

        categorias = list(Categoria.objects.all())
        proveedores = list(Proveedor.objects.all())

        # 4. Generación masiva optimizada por bloques (bulk_create para que vuele con 100 mil o 1 millón)
        batch_size = 5000
        productos_lote = []

        for i in range(cantidad):
            productos_lote.append(
                Producto(
                    nombre=f"{fake.unique.word().capitalize()} Pro {i}",
                    precio=fake.random_int(min=20000, max=800000),
                    stock=fake.random_int(min=5, max=100),
                    categoria=fake.random_element(categorias),
                    proveedor=fake.random_element(proveedores)
                )
            )
            # Si el lote llega al límite, se guarda de golpe en la base de datos para optimizar memoria
            if len(productos_lote) >= batch_size:
                Producto.objects.bulk_create(productos_lote)
                productos_lote = []

        # Guardar los que queden pendientes
        if productos_lote:
            Producto.objects.bulk_create(productos_lote)

        self.stdout.write(self.style.SUCCESS(f'¡Se han generado e insertado exitosamente {cantidad} productos con Faker!'))