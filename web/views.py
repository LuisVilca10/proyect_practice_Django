from django.shortcuts import render,get_object_or_404, redirect
from .carrito import Cart

from .models import Categoria, Producto


# Create your views here.
#vitsa producto
def index(request):
    listacategoria = Categoria.objects.all()
    listaproducto= Producto.objects.all()
    #print(listaproducto)
    context = {
        'productos':listaproducto,
        'categorias' : listacategoria
    }
    return render(request, 'index.html', context,)

def productosporcategoria(request, categoria_id):
    #fir¿ltrado de productos por categoria
    objCategoria = Categoria.objects.get(pk=categoria_id)
    listaproducto= objCategoria.producto_set.all()
    listacategoria = Categoria.objects.all()
    context = {
        'categorias' : listacategoria,
        'productos':listaproducto
    }
    return render(request, 'index.html', context)

def productosPorNombre(request):
    #filtrado por nombre
    nombre = request.POST['nombre']

    listaproducto= Producto.objects.filter(nombre__contains=nombre)
    listacategoria = Categoria.objects.all()
    context = {
        'categorias' : listacategoria,
        'productos':listaproducto
    }
    return render(request, 'index.html', context)

def productoDetalle(request, producto_id):
    #detalle producto
    #objProducto = Producto.objects.get(pk=producto_id)
    objProducto = get_object_or_404(Producto,pk=producto_id)
    context = {
        'productos': objProducto
    }

    return render(request, 'producto.html', context)


"""carrito de compras"""


def carrito(request):
    return render(request, 'carrito.html')

def agregarCarrito(request, producto_id):
    #cantidad = 1

    if request.method == 'POST':
        cantidad = int(request.POST['cantidad'])
    else:
        cantidad = 1
    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    if objProducto.imagen and objProducto.imagen.file:
        imagen_url = objProducto.imagen.url
    else:
        imagen_url = 'https://via.placeholder.com/150'
    carritoProducto.add(objProducto, cantidad)

    #print(request.session.get("cart"))
    if request.method == 'GET':
        return redirect('/')
    return render(request, 'carrito.html')

def eliminarProductoCarrito(request, producto_id):
    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.delete(objProducto)
    
    return render(request, 'carrito.html')

def limpiarCarrito(request):
    carritoProducto = Cart(request)
    carritoProducto.clear()
    
    return render(request, 'carrito.html')