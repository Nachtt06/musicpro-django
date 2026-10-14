from django.core.management.base import BaseCommand
from faker import Faker
from core.models import Rol, UsuarioSistema, Categoria, Proveedor, Producto, Cliente

class Command(BaseCommand):
    help = 'Genera datos masivos usando Faker para el sistema MusicPro'

    def handle(self, *args, **options):
        fake = Faker('es_CL')
        Faker.seed(42)

        self.stdout.write(self.style.WARNING('Iniciando carga de datos masivos...'))

        roles_nombres = ['Administrador', 'Vendedor', 'Bodeguero']
        for r_nombre in roles_nombres:
            Rol.objects.get_or_create(nombre=r_nombre)
        self.stdout.write(self.style.SUCCESS('Roles creados exitosamente.'))

        categorias_nombres = ['Cuerdas', 'Percusión', 'Teclados', 'Viento', 'Audio e Iluminación']
        for cat_nombre in categorias_nombres:
            Categoria.objects.get_or_create(nombre=cat_nombre, defaults={'descripcion': fake.sentence()})
        self.stdout.write(self.style.SUCCESS('Categorías creadas exitosamente.'))

        for _ in range(5):
            Proveedor.objects.get_or_create(
                razon_social=fake.company(),
                defaults={
                    'telefono': fake.phone_number(),
                    'email': fake.company_email()
                }
            )
        self.stdout.write(self.style.SUCCESS('Proveedores creados exitosamente.'))

        categorias = list(Categoria.objects.all())
        proveedores = list(Proveedor.objects.all())

        for _ in range(20):
            Producto.objects.create(
                nombre=fake.unique.word().capitalize() + " Pro",
                precio=fake.random_int(min=20000, max=800000),
                stock=fake.random_int(min=5, max=100),
                categoria=fake.random_element(categorias),
                proveedor=fake.random_element(proveedores)
            )
        self.stdout.write(self.style.SUCCESS('¡20 Productos creados con éxito mediante Faker!'))