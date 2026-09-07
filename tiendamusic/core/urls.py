from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('catalogo/', views.catalogo_view, name='catalogo'),
    path('producto/<int:producto_id>/', views.detalle_producto_view, name='detalle_producto'),
    path('carrito/', views.carrito_view, name='carrito'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('confirmacion/', views.confirmacion_orden_view, name='confirmacion_orden'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('historial/', views.historial_compras_view, name='historial_compras'),
    path('admin-tienda/productos/', views.admin_panel_view, name='admin_panel'),
    path('admin-tienda/productos/', views.admin_panel_view, name='admin_productos'), # Alias para evitar NoReverseMatch
    path('admin-tienda/usuarios/', views.admin_usuarios_view, name='admin_usuarios'),
]