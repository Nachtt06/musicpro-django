import json
import os
from django.shortcuts import render, redirect
from django.conf import settings

def cargar_json(nombre_archivo):
    json_path = os.path.join(settings.BASE_DIR, 'core', 'data', nombre_archivo)
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

# Autenticación
def login_view(request):
    error = None
    if request.method == 'POST':
        usuario_input = request.POST.get('username')
        password_input = request.POST.get('password')
        usuarios = cargar_json('usuarios.json')
        user_encontrado = next((u for u in usuarios if u['username'] == usuario_input and u['password'] == password_input), None)
        
        if user_encontrado:
            request.session['usuario'] = user_encontrado
            return redirect('admin_panel' if user_encontrado['rol'] == 'admin' else 'home')
        else:
            error = "Usuario o contraseña incorrectos"
            
    return render(request, 'login.html', {'error': error})

def logout_view(request):
    request.session.flush()
    return redirect('login')

# Vistas de Cliente
def home_view(request):
    usuario = request.session.get('usuario')
    if not usuario:
        return redirect('login')
    productos = cargar_json('productos.json')
    return render(request, 'home.html', {'productos': productos, 'usuario': usuario})

def catalogo_view(request):
    usuario = request.session.get('usuario')
    if not usuario:
        return redirect('login')
    productos = cargar_json('productos.json')
    return render(request, 'index.html', {'productos': productos, 'usuario': usuario})

def detalle_producto_view(request, producto_id):
    usuario = request.session.get('usuario')
    if not usuario:
        return redirect('login')
    productos = cargar_json('productos.json')
    producto = next((p for p in productos if p['id'] == producto_id), None)
    return render(request, 'detalle_producto.html', {'producto': producto, 'usuario': usuario})

def carrito_view(request):
    usuario = request.session.get('usuario')
    if not usuario:
        return redirect('login')
    productos = cargar_json('productos.json')[:2]
    total = sum(p['precio'] for p in productos)
    return render(request, 'carrito.html', {'productos': productos, 'total': total, 'usuario': usuario})

def checkout_view(request):
    usuario = request.session.get('usuario')
    if not usuario:
        return redirect('login')
    return render(request, 'checkout.html', {'usuario': usuario})

def confirmacion_orden_view(request):
    usuario = request.session.get('usuario')
    if not usuario:
        return redirect('login')
    return render(request, 'confirmacion_orden.html', {'usuario': usuario})

def perfil_view(request):
    usuario = request.session.get('usuario')
    if not usuario:
        return redirect('login')
    return render(request, 'perfil.html', {'usuario': usuario})

def historial_compras_view(request):
    usuario = request.session.get('usuario')
    if not usuario:
        return redirect('login')
    return render(request, 'historial_compras.html', {'usuario': usuario})

# Vistas de Administrador
def admin_panel_view(request):
    usuario = request.session.get('usuario')
    if not usuario or usuario['rol'] != 'admin':
        return redirect('login')
    productos = cargar_json('productos.json')
    return render(request, 'admin_panel.html', {'productos': productos, 'usuario': usuario})

def admin_usuarios_view(request):
    usuario = request.session.get('usuario')
    if not usuario or usuario['rol'] != 'admin':
        return redirect('login')
    usuarios = cargar_json('usuarios.json')
    return render(request, 'admin_usuarios.html', {'usuarios': usuarios, 'usuario': usuario})