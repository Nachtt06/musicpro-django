import json
import os
from django.shortcuts import render, redirect
from django.conf import settings

# Rutas de los archivos JSON de datos
BASE_DIR = settings.BASE_DIR
DATA_DIR = os.path.join(BASE_DIR, 'core', 'data')
PRODUCTOS_FILE = os.path.join(DATA_DIR, 'productos.json')
USUARIOS_FILE = os.path.join(DATA_DIR, 'usuarios.json')

# Funciones auxiliares para leer y escribir JSON
def cargar_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def guardar_json(filepath, data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- VISTAS DE AUTENTICACIÓN ---

def login_view(request):
    error = None
    if request.method == 'POST':
        username_input = request.POST.get('usuario') or request.POST.get('email') or request.POST.get('username')
        password = request.POST.get('password')
        
        usuarios = cargar_json(USUARIOS_FILE)
        
        user_encontrado = next(
            (u for u in usuarios if (u.get('usuario') == username_input or u.get('email') == username_input) and u.get('password') == password),
            None
        )
        
        if user_encontrado:
            request.session['usuario_id'] = user_encontrado['id']
            request.session['usuario_nombre'] = user_encontrado.get('nombre', user_encontrado.get('usuario'))
            request.session['rol'] = user_encontrado['rol']
            
            if user_encontrado['rol'] == 'admin':
                return redirect('admin_panel')
            return redirect('home')
        else:
            error = "Correo o contraseña incorrectos."
            
    return render(request, 'login.html', {'error': error})

def logout_view(request):
    request.session.flush()
    return redirect('login')

# --- VISTAS DE CLIENTE ---

def home_view(request):
    productos = cargar_json(PRODUCTOS_FILE)
    destacados = productos[:3]
    return render(request, 'home.html', {'productos': destacados})

def catalogo_view(request):
    productos = cargar_json(PRODUCTOS_FILE)
    return render(request, 'catalogo.html', {'productos': productos})

def detalle_producto_view(request, producto_id):
    productos = cargar_json(PRODUCTOS_FILE)
    producto = next((p for p in productos if p['id'] == producto_id), None)
    return render(request, 'detalle_producto.html', {'producto': producto})

def carrito_view(request):
    carrito = request.session.get('carrito', [])
    return render(request, 'carrito.html', {'carrito': carrito})

def checkout_view(request):
    return render(request, 'checkout.html')

def confirmacion_orden_view(request):
    request.session['carrito'] = []
    return render(request, 'confirmacion_orden.html')

def perfil_view(request):
    usuario_id = request.session.get('usuario_id')
    usuarios = cargar_json(USUARIOS_FILE)
    usuario = next((u for u in usuarios if u['id'] == usuario_id), None)
    return render(request, 'perfil.html', {'usuario': usuario})

def historial_compras_view(request):
    return render(request, 'historial_compras.html')

# --- VISTAS DE ADMINISTRADOR ---

def admin_panel_view(request):
    if request.session.get('rol') != 'admin':
        return redirect('home')
        
    productos = cargar_json(PRODUCTOS_FILE)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = float(request.POST.get('precio', 0))
        descripcion = request.POST.get('descripcion')
        
        nuevo_id = max([p['id'] for p in productos], default=0) + 1
        nuevo_producto = {
            "id": nuevo_id,
            "nombre": nombre,
            "precio": precio,
            "descripcion": descripcion,
            "imagen": "https://via.placeholder.com/300"
        }
        productos.append(nuevo_producto)
        guardar_json(PRODUCTOS_FILE, productos)
        return redirect('admin_panel')
        
    return render(request, 'admin_panel.html', {'productos': productos})

def admin_usuarios_view(request):
    if request.session.get('rol') != 'admin':
        return redirect('home')
        
    usuarios = cargar_json(USUARIOS_FILE)
    return render(request, 'admin_usuarios.html', {'usuarios': usuarios})
