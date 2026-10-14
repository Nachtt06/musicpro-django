from django.contrib import admin
from .models import (
    Rol, UsuarioSistema, Categoria, Proveedor, Producto,
    Cliente, Venta, DetalleVenta, InventarioLog, ConfiguracionSistema
)

class RolAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    list_per_page = 10

admin.site.register(Rol, RolAdmin)


class UsuarioSistemaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'email', 'rol', 'activo')
    search_fields = ('nombre', 'email')
    list_filter = ('rol', 'activo')
    list_per_page = 10

admin.site.register(UsuarioSistema, UsuarioSistemaAdmin)


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)
    list_per_page = 10

admin.site.register(Categoria, CategoriaAdmin)


class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('id', 'razon_social', 'telefono', 'email')
    search_fields = ('razon_social',)
    list_per_page = 10

admin.site.register(Proveedor, ProveedorAdmin)


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'stock', 'categoria', 'proveedor')
    search_fields = ('nombre',)
    list_filter = ('categoria', 'proveedor')
    list_editable = ('precio', 'stock')
    list_per_page = 10

admin.site.register(Producto, ProductoAdmin)


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'rut', 'nombre', 'email', 'direccion')
    search_fields = ('rut', 'nombre', 'email')
    list_per_page = 10

admin.site.register(Cliente, ClienteAdmin)


class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'cliente', 'usuario', 'total')
    list_filter = ('fecha', 'usuario')
    list_per_page = 10

admin.site.register(Venta, VentaAdmin)


class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'venta', 'producto', 'cantidad', 'subtotal')
    list_per_page = 10

admin.site.register(DetalleVenta, DetalleVentaAdmin)


class InventarioLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'stock_anterior', 'stock_nuevo', 'fecha_cambio')
    list_filter = ('fecha_cambio',)
    list_per_page = 10

admin.site.register(InventarioLog, InventarioLogAdmin)


class ConfiguracionSistemaAdmin(admin.ModelAdmin):
    list_display = ('id', 'clave', 'valor')
    search_fields = ('clave',)
    list_per_page = 10

admin.site.register(ConfiguracionSistema, ConfiguracionSistemaAdmin)