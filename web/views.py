from django.shortcuts import render,get_object_or_404, redirect
from .carrito import Cart

from .models import Categoria, Producto, Cliente, Pedido, PedidoDetalle
from django.contrib.auth.models import User
from .forms import ClienteForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse


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

"""Gestión para clientes y usuarios"""

def crearUsuario(request):
    
    if request.method == 'POST':
        dataUsuario = request.POST['nuevoUsuario']
        dataPassword = request.POST['nuevoPassword']
        
        nuevoUsuario = User.objects.create_user(username=dataUsuario,password=dataPassword)
        if nuevoUsuario is not None:
            login(request,nuevoUsuario)
            return redirect('/cuenta')
    
    
    return render(request,'login.html')

def logoutUsuario(request):
    logout(request)
    return render(request,'login.html')

def cuentaUsuario(request):
    try:
        clienteEditar = Cliente.objects.get(usuario = request.user)
        
        dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'emial':request.user.email,
            'direccion':clienteEditar.direccion,
            'telefono':clienteEditar.telefono,
            'dni':clienteEditar.dni,
            'sexo':clienteEditar.sexo,
            'fecha_nacimiento':clienteEditar.fecha_nacimiento
        }
    except:
         dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'emial':request.user.email,
            'direccion':clienteEditar.direccion,
            'telefono':clienteEditar.telefono,
            'dni':clienteEditar.dni,
            'sexo':clienteEditar.sexo,
            'fecha_nacimiento':clienteEditar.fecha_nacimiento
         }

    frmCliente = ClienteForm(dataCliente)
    context = {
        'frmCliente':frmCliente
    }
    
    return render(request,'cuenta.html',context)

def loginUsuario(request):
    paginaDestino = request.GET.get('next',None)
    context = {
         'destino':paginaDestino
    }
    
    if request.method == 'POST':
        dataUsuario = request.POST['usuario']
        dataPassword = request.POST['password']
        dataDestino = request.POST['destino']
        
        usuarioAuth = authenticate(request,username=dataUsuario,password=dataPassword)
        if usuarioAuth is not None:
            login(request,usuarioAuth)

            if dataDestino != 'None':
                return redirect(dataDestino)
            
            return redirect('/cuenta')
        else:
            context = {
                'mensajeError':'Datos incorrectos'
            }
    
    return render(request,'login.html',context)

def actualizarCliente(request):
    mensaje = ""
    frmCliente = ClienteForm()  # Inicializar el formulario antes del bloque if
    
    if request.method == "POST":
        frmCliente = ClienteForm(request.POST)
        if frmCliente.is_valid():
            datacliente = frmCliente.cleaned_data
            # Actualizar usuario
            actUsuario = User.objects.get(pk=request.user.id)
            actUsuario.first_name = datacliente["nombre"]
            actUsuario.last_name = datacliente["apellidos"]
            actUsuario.email = datacliente["emial"]
            actUsuario.save()
            
            # Registrar Cliente
            nuevoCliente = Cliente()
            nuevoCliente.usuario = actUsuario
            nuevoCliente.dni = datacliente["dni"]
            nuevoCliente.direccion = datacliente["direccion"]
            nuevoCliente.telefono = datacliente["telefono"]
            nuevoCliente.sexo = datacliente["sexo"]
            nuevoCliente.fecha_nacimiento = datacliente["fecha_nacimiento"]
            nuevoCliente.save()
            
            mensaje = "Datos Actualizados"
        else:
            # Manejar el caso de formulario no válido
            mensaje = "Error: Por favor, corrige los errores en el formulario."
            
    context ={
        'mensaje': mensaje,
        'frmCliente': frmCliente
    }

    return render(request, 'cuenta.html', context)

"""lista pra el procesos de compras"""
@login_required(login_url='/login')
def registrarPedido(request):
    try:
        clienteEditar = Cliente.objects.get(usuario = request.user)
        
        dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email,
            'direccion':clienteEditar.direccion,
            'telefono':clienteEditar.telefono,
            'dni':clienteEditar.dni,
            'sexo':clienteEditar.sexo,
            'fecha_nacimiento':clienteEditar.fecha_nacimiento
        }
    except:
         dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email
         }
    
    frmCliente = ClienteForm(dataCliente)
    context = {
        'frmCliente':frmCliente
    }
    
    return render(request,'pedido.html',context)

def view_that_asks_for_money(request):

    # What you want the button to do.
    paypal_dict = {
        "business": "sb-kco47c26748133@business.example.com",
        "amount": "10.00",
        "item_name": "prueba edshop",
        "invoice": "10-edshop",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri('/'),
        "cancel_return": request.build_absolute_uri('/logout'),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment.html", context)

@login_required(login_url='/login')
def confirmarPedido(request):
    context = {}
    if request.method == "POST":
                        
            #actualizar usuario
            actUsuario = User.objects.get(pk=request.user.id)
            actUsuario.first_name = request.POST["nombre"]
            actUsuario.last_name = request.POST["apellidos"]
            actUsuario.save()
                
            try:
                clientePedido = Cliente.objects.get(usuario = request.user)
                clientePedido.telefono = request.POST["telefono"]
                clientePedido.direccion = request.POST["direccion"]
                clientePedido.save()
            except:
                clientePedido = Cliente()
                clientePedido.usuario = actUsuario
                clientePedido.direccion = request.POST["direccion"]
                clientePedido.telefono = request.POST["telefono"]
                clientePedido.save()
                
            #registrar pedido
            nroPedido = ''
            montoTotal = 0
            nuevoPedido = Pedido()
            nuevoPedido.cliente = clientePedido
            nuevoPedido.save()
            
            
            #actualizar pedido
            nroPedido = 'PED' + nuevoPedido.fecha_registro.strftime('%Y') + str(nuevoPedido.id)
            nuevoPedido.nro_pedido = nroPedido
            nuevoPedido.monto_total = montoTotal
            nuevoPedido.save()
            
                
            context = {
                'pedido':nuevoPedido,
            }
        
    return render(request,'compra.html', context)