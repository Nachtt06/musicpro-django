from django.contrib import admin
from .models import (
    Rol, UsuarioSistema, Categoria, Proveedor, Producto,
    Cliente, Venta, DetalleVenta, InventarioLog, ConfiguracionSistema
)

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(UsuarioSistema)
class UsuarioSistemaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email', 'rol', 'activo')
    search_fields = ('nombre', 'email')
    list_filter = ('rol', 'activo')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('id', 'razon_social', 'telefono', 'email')
    search_fields = ('razon_social',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'stock', 'categoria', 'proveedor')
    search_fields = ('nombre',)
    list_filter = ('categoria', 'proveedor')
    list_editable = ('precio', 'stock')
    list_per_page = 10

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'rut', 'nombre', 'email', 'direccion')
    search_fields = ('rut', 'nombre', 'email')
    list_per_page = 15

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'cliente', 'usuario', 'total')
    list_filter = ('fecha',)

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'venta', 'producto', 'cantidad', 'subtotal')

@admin.register(InventarioLog)
class InventarioLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'stock_anterior', 'stock_nuevo', 'fecha_cambio')
    list_filter = ('fecha_cambio',)

@admin.register(ConfiguracionSistema)
class ConfiguracionSistemaAdmin(admin.ModelAdmin):
    list_display = ('id', 'clave', 'valor')
    search_fields = ('clave',)