from django.shortcuts import render, get_object_or_404

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

