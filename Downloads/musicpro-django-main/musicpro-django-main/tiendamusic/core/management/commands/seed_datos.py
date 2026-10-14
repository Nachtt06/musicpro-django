from django.core.management.base import BaseCommand
from faker import Faker
from core.models import Rol, UsuarioSistema, Categoria, Proveedor, Producto, Cliente

class Command(BaseCommand):
    help = 'Genera datos masivos de productos y clientes usando Faker'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cantidad',
            type=int,
            default=20,
            help='Número de registros a generar'
        )

    @staticmethod
    def _rut_con_digito_verificador(numero):
        suma = 0
        multiplicador = 2
        for digito in reversed(str(numero)):
            suma += int(digito) * multiplicador
            multiplicador = 2 if multiplicador == 7 else multiplicador + 1

        digito_verificador = 11 - suma % 11
        if digito_verificador == 11:
            dv = "0"
        elif digito_verificador == 10:
            dv = "K"
        else:
            dv = str(digito_verificador)
        return f"{numero}-{dv}"

    def handle(self, *args, **options):
        cantidad = options['cantidad']
        fake = Faker('es_CL')
        Faker.seed(42)

        self.stdout.write(self.style.WARNING(f'Iniciando carga masiva de {cantidad} registros...'))

        # 1. Asegurar Roles y Categorías base
        for r_nombre in ['Administrador', 'Vendedor', 'Bodeguero']:
            Rol.objects.get_or_create(nombre=r_nombre)

        for cat_nombre in ['Cuerdas', 'Percusión', 'Teclados', 'Viento', 'Audio e Iluminación']:
            Categoria.objects.get_or_create(nombre=cat_nombre, defaults={'descripcion': fake.sentence()})

        for _ in range(10):
            Proveedor.objects.get_or_create(
                razon_social=fake.company(),
                defaults={'telefono': fake.phone_number(), 'email': fake.company_email()}
            )

        categorias = list(Categoria.objects.all())
        proveedores = list(Proveedor.objects.all())

        batch_size = 5000
        productos_lote = []
        clientes_lote = []

        for i in range(cantidad):
            # Crear lote de productos
            productos_lote.append(
                Producto(
                    nombre=f"{fake.unique.word().capitalize()} Pro {i}",
                    precio=fake.random_int(min=20000, max=800000),
                    stock=fake.random_int(min=5, max=100),
                    categoria=fake.random_element(categorias),
                    proveedor=fake.random_element(proveedores)
                )
            )

            # Crear lote de clientes (con RUT chileno válido simulado)
            rut_base = fake.random_int(min=10_000_000, max=25_000_000)
            rut_generado = self._rut_con_digito_verificador(rut_base)
            
            clientes_lote.append(
                Cliente(
                    rut=rut_generado,
                    nombre=fake.name()[:100],
                    email=fake.unique.safe_email()[:100],
                    direccion=fake.address()[:200]
                )
            )

            if len(productos_lote) >= batch_size:
                Producto.objects.bulk_create(productos_lote, ignore_conflicts=True)
                Cliente.objects.bulk_create(clientes_lote, ignore_conflicts=True)
                productos_lote = []
                clientes_lote = []

        if productos_lote:
            Producto.objects.bulk_create(productos_lote, ignore_conflicts=True)
            Cliente.objects.bulk_create(clientes_lote, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(f'¡Se han generado e insertado exitosamente {cantidad} productos y clientes con Faker!'))