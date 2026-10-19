from django.db import models

# Create your models here.
from django.db import models

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre de Rol")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        ordering = ["nombre"]


class UsuarioSistema(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre Completo")
    email = models.EmailField(max_length=100, unique=True, verbose_name="Correo Electrónico")
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, verbose_name="Rol Asignado")
    activo = models.BooleanField(default=True, verbose_name="Estado Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    def __str__(self):
        return f"{self.nombre} ({self.email})"

    class Meta:
        verbose_name = "Usuario del Sistema"
        verbose_name_plural = "Usuarios del Sistema"
        ordering = ["nombre"]


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de Categoría")
    descripcion = models.CharField(max_length=200, null=True, blank=True, verbose_name="Descripción")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]


class Proveedor(models.Model):
    razon_social = models.CharField(max_length=150, unique=True, verbose_name="Razón Social")
    telefono = models.CharField(max_length=15, null=True, blank=True, verbose_name="Teléfono")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="Correo")

    def __str__(self):
        return self.razon_social

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ["razon_social"]


class Producto(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre del Producto")
    precio = models.IntegerField(verbose_name="Precio Unitario")
    stock = models.IntegerField(verbose_name="Stock Disponible")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoría")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, verbose_name="Proveedor")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["nombre"]


class Cliente(models.Model):
    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT del Cliente")
    nombre = models.CharField(max_length=100, verbose_name="Nombre Completo")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="Correo")
    direccion = models.CharField(max_length=200, null=True, blank=True, verbose_name="Dirección")

    def __str__(self):
        return f"{self.rut} - {self.nombre}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["nombre"]


class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    usuario = models.ForeignKey(UsuarioSistema, on_delete=models.CASCADE, verbose_name="Atendido por")
    total = models.IntegerField(default=0, verbose_name="Monto Total")

    def __str__(self):
        return f"Venta #{self.id} - Total: ${self.total}"

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ["-fecha"]


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, verbose_name="Venta")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Producto")
    cantidad = models.IntegerField(verbose_name="Cantidad")
    subtotal = models.IntegerField(verbose_name="Subtotal")

    def __str__(self):
        return f"Detalle #{self.id} (Venta #{self.venta.id})"

    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Ventas"


class InventarioLog(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Producto")
    stock_anterior = models.IntegerField(verbose_name="Stock Anterior")
    stock_nuevo = models.IntegerField(verbose_name="Stock Nuevo")
    fecha_cambio = models.DateTimeField(auto_now_add=True, verbose_name="Fecha del Cambio")

    def __str__(self):
        return f"Log: {self.producto.nombre} ({self.stock_anterior} -> {self.stock_nuevo})"

    class Meta:
        verbose_name = "Registro de Inventario"
        verbose_name_plural = "Registros de Inventario"
        ordering = ["-fecha_cambio"]


class ConfiguracionSistema(models.Model):
    clave = models.CharField(max_length=100, unique=True, verbose_name="Clave de Configuración")
    valor = models.CharField(max_length=255, verbose_name="Valor")

    def __str__(self):
        return self.clave

    class Meta:
        verbose_name = "Configuración del Sistema"
        verbose_name_plural = "Configuraciones del Sistema"
