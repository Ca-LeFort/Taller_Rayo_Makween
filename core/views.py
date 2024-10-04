from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from .serializers import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
import requests
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from io import BytesIO
from .funciones import miindicadorAPI, paisAPI
# Create your views here.

# APIS
class TipoServicioViewset(viewsets.ModelViewSet):
	queryset = TipoServicio.objects.all()
	serializer_class = TipoServicioSerializers
	renderer_classes = [JSONRenderer]

class MecanicoViewset(viewsets.ModelViewSet):
	queryset = Mecanico.objects.all()
	serializer_class = MecanicoSerializers
	renderer_classes = [JSONRenderer]

class ClienteViewset(viewsets.ModelViewSet):
	queryset = Cliente.objects.all()
	serializer_class = ClienteSerializers
	renderer_classes = [JSONRenderer]

class TrabajoViewset(viewsets.ModelViewSet):
	queryset = Trabajo.objects.all()
	serializer_class = TrabajoSerializers
	renderer_classes = [JSONRenderer]

class EstadoTrabajoViewset(viewsets.ModelViewSet):
	queryset = EstadoTrabajo.objects.all()
	serializer_class = EstadoTrabajoSerializers
	renderer_classes = [JSONRenderer]

class TipoConsultasViewset(viewsets.ModelViewSet):
	queryset = TipoConsulta.objects.all()
	serializer_class = TipoConsultaSerializers
	renderer_classes = [JSONRenderer]

class ContactoViewset(viewsets.ModelViewSet):
	queryset = Contacto.objects.all()
	serializer_class = ContactoSerializers
	renderer_classes = [JSONRenderer]

class ReservaViewset(viewsets.ModelViewSet):
	queryset = Reserva.objects.all()
	serializer_class = ReservaSerializers
	renderer_classes = [JSONRenderer]

class PagoReservaViewset(viewsets.ModelViewSet):
	queryset = Pago_reserva.objects.all()
	serializer_class = PagoReservaSerializers
	renderer_classes = [JSONRenderer]

class CarritoViewset(viewsets.ModelViewSet):
	queryset = Carrito.objects.all()
	serializer_class = CarritoSerializers
	renderer_classes = [JSONRenderer]

# CONSUMO DE APIS
#def mecanicosapi(request):
    #response = requests.get('https://proyecto-taller-makween-django.vercel.app/api/mecanico/')
    #mecanicos = response.json()
    #aux = {
    #    'lista' : mecanicos
    #}

    #return render(request, 'core/mecanicos/crudapi/listar.html', aux)

#def mecanicodetalle(request, id):
#    #response = requests.get(f'https://proyecto-taller-makween-django.vercel.app/api/mecanico/{id}/')
#    mecanico = response.json()
#
#    return render(request, 'core/mecanicos/crudapi/detalle.html', {'mecanico' : mecanico})

# VISTAS
def index(request):
    trabajos = Trabajo.objects.all().order_by('-id')
    aux = {
        'lista' : trabajos
    }

    return render(request, 'core/index.html', aux)

def account_locked(request):
    return render(request, 'core/account_locked.html')

def nosotros(request):
    mecanicos = Mecanico.objects.all()
    aux = {
        'lista' : mecanicos
    }

    return render(request, 'core/nosotros.html', aux)

def servicios(request):
    tiposervicios = TipoServicio.objects.all()
    aux = {
        'lista' : tiposervicios
    }

    return render(request, 'core/servicios.html', aux)

def contacto(request):
    aux = {
        'form' : ContactoForm()
    }

    if request.method == 'POST':
        formulario = ContactoForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            aux['msj'] = 'Enviado'
        else:
            aux['form'] = formulario
            aux['msj'] = 'No se pudo enviar'

    return render(request, 'core/contacto.html', aux)

def login(request):
    aux = {
        'form' : CustomAuthentication()
    }

    if request.method == 'POST':
        formulario = CustomAuthentication(request.POST)
        if formulario.is_valid():
            messages.success(request, "Bienvenido")
            return redirect(to="index")
        else:
            aux['form'] = formulario
            messages.error(request, "No se pudo iniciar sesión")
    
    return render(request, 'registration/login.html', aux)

def logout_view(request):
    logout(request)

def register(request):
    aux = {
        'form' : CustomUserCreationForm()
    }
    cliente = Cliente()

    if request.method == 'POST':
        formulario = CustomUserCreationForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()
            group = Group.objects.get(name="Cliente")
            user.groups.add(group)
            cliente.nombre_cliente = user.first_name
            cliente.apellido_cliente = user.last_name
            cliente.correo_cliente = user.email
            cliente.save()
            messages.success(request, 'Usuario creado correctamente!')
            return redirect(to="login")
        else:
            aux['form'] = formulario
            messages.error(request, 'No se pudo registrar')

    return render(request, 'registration/register.html', aux)

@login_required
def mecanicos(request):
    mecanicos = Mecanico.objects.all()
    for mec in mecanicos:
        mec.cant_mantenciones_mec = mec.calcular_cantidad_trabajos()
        mec.save()

    # PAGINATOR
    paginator = Paginator(mecanicos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    aux = {
        'page_obj' : page_obj
    }
    return render(request, 'core/mecanicos/crud_mecanico/listar.html', aux)

def galeria(request):
    trabajos = Trabajo.objects.all()

    # PAGINATOR
    paginator = Paginator(trabajos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    aux = {
        'page_obj' : page_obj
    }
    return render(request, 'core/galeria.html',aux)

def not_found(request):
    return render(request, 'core/404.html')

@permission_required('core.add_mecanico')
def mecanicoadd(request):
    aux = {
        'form' : MecanicoForm()
    }

    if request.method == 'POST':
        formulario = MecanicoForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Mecánico almacenado correctamente!")
        else:
            aux['form'] = formulario
            messages.error(request, "No se pudo almacenar el mecánico!")

    return render(request, 'core/mecanicos/crud_mecanico/add.html', aux)

@permission_required('core.change_mecanico')
def mecanicoupdate(request, id):
    mecanico = Mecanico.objects.get(id=id)
    aux = {
        'form' : MecanicoForm(instance=mecanico)
    }

    if request.method == 'POST':
        formulario = MecanicoForm(data=request.POST, instance=mecanico)
        if formulario.is_valid():
            formulario.save()
            aux['form'] = formulario
            messages.success(request, "Mecánico modificado correctamente!")
            return redirect(to="mecanicolistar")
        else:
            aux['form'] = formulario
            messages.error(request, "No se pudo modificar el mecánico!")

    return render(request, 'core/mecanicos/crud_mecanico/update.html', aux)

@permission_required('core.delete_mecanico')
def mecanicodelete(request, id):
    mecanico = Mecanico.objects.get(id=id)
    mecanico.delete()

    return redirect(to="mecanicos")

@permission_required('core.add_trabajo')
def trabajoadd(request):
    aux = {
        'form' : TrabajoForm()
    }

    if request.method == 'POST':
        formulario = TrabajoForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Proyecto almacenado correctamente!")
        else:
            aux['form'] = formulario
            messages.error(request, "No se pudo almacenar el proyecto!")

    return render(request, 'core/mecanicos/crud_proyecto/add.html', aux)

@permission_required('core.view_trabajo')
def trabajos(request):
    trabajos = Trabajo.objects.all().order_by('-id')

    # PAGINATOR
    paginator = Paginator(trabajos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    aux = {
        'page_obj' : page_obj
    }

    return render(request, 'core/mecanicos/crud_proyecto/listar.html', aux)

@permission_required('core.change_trabajo')
def trabajoupdate(request, id):
    trabajos = Trabajo.objects.get(id=id)
    aux = {
        'form' : TrabajoAdminForm(instance=trabajos)
    }

    if request.method == 'POST':
        formulario = TrabajoAdminForm(data=request.POST, instance=trabajos)
        if formulario.is_valid():
            formulario.save()
            aux['form'] = formulario
            messages.success(request, "Trabajo aplicado correctamente!")
            return redirect(to="trabajolistar")
        else:
            aux['form'] = formulario
            messages.error(request, "No se pudo aplicar el estado de trabajo!")

    return render(request, 'core/mecanicos/crud_proyecto/update.html', aux)

def trabajo(request, id):
    trabajo = Trabajo.objects.get(id=id,estado_publicacion='A')
    aux = {
        'lista' : trabajo
    }
    return render(request, 'core/trabajo.html', aux)

def listarconsultas(request):
    consultas = Contacto.objects.all()

    # PAGINATOR
    paginator = Paginator(consultas, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    aux = {
        'page_obj' : page_obj
    }

    return render(request, 'core/mecanicos/consultas.html', aux)

def listarreservas(request):
    reservas = Reserva.objects.all().order_by('-id')
    aux = {
        'lista' : reservas
    }

    return render(request, 'core/mecanicos/reservas.html', aux)

@login_required
def reserva(request):
    aux = {
        'form' : ReservaForm
    }

    if request.method == 'POST':
        formulario = ReservaForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Reservado")
        else:
            aux['form'] = formulario
            messages.error(request, "No se pudo reservar")

    return render(request, 'core/reserva.html', aux)

def reservaupdate(request, id):
    reservas = Reserva.objects.get(id=id)
    aux = {
        'form' : ReservaAdminForm(instance=reservas)
    }

    if request.method == 'POST':
        formulario = ReservaAdminForm(data=request.POST, instance=reservas)
        if formulario.is_valid():
            formulario.save()
            aux['form'] = formulario
            messages.success(request, "Reserva aplicado correctamente!")
        else:
            aux['form'] = formulario
            messages.error(request, "No se pudo aplicar la reserva!")

    return render(request, 'core/mecanicos/reservaupdate.html', aux)

def categoria_trabajo(request, id):
    tipo_servicio = get_object_or_404(TipoServicio, id=id)
    trabajos = Trabajo.objects.filter(servicio=tipo_servicio, estado_publicacion='A').order_by('-id')

    # PAGINATOR
    paginator = Paginator(trabajos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tipo_servicio': tipo_servicio,
        'page_obj': page_obj
    }
    
    return render(request, 'core/cat_trabajo.html', context)

def mecanico_trabajo(request, id):
    mecanico = get_object_or_404(Mecanico, id=id)
    trabajos = Trabajo.objects.filter(mecanico=mecanico, estado_publicacion='A').order_by('-id')

    # PAGINATOR
    paginator = Paginator(trabajos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'mecanico' : mecanico,
        'page_obj' : page_obj
    }

    return render(request, 'core/mec_trabajo.html', context)


def buscador(request):
    form = TrabajoSearchForm()
    trabajos = []

    if 'query' in request.GET:
        form = TrabajoSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            trabajos = Trabajo.objects.filter(
                Q(nombre_trabajo__icontains=query) |
                Q(diagnostico__icontains=query) |
                Q(mecanico__nombre_mecanico__icontains=query) |
                Q(fecha__icontains=query) |
                Q(materiales__icontains=query) |
                Q(servicio__descripcion__icontains=query), estado_publicacion='A'
            )

    return render(request, 'core/buscador.html', {'form': form, 'trabajos': trabajos})

def pagina_404(request, exception=None):
    return render(request, 'core/404.html', status=404)

def clientes(request):
    clientes = Cliente.objects.all()
    for cli in clientes:
        cli.cant_mantenciones_cli = cli.calcular_cantidad_trabajos()
        cli.save()
    aux = {
        'lista' : clientes
    }
    return render(request, 'core/mecanicos/crud_clientes/listar.html', aux)

@login_required
def res_servicios(request):
    precio1 = round(miindicadorAPI(indicador='dolar') * 2.5)
    precio2 = round(miindicadorAPI(indicador='dolar') * 10)
    precio3 = round(miindicadorAPI(indicador='dolar') * 8.5)
    precio4 = round(miindicadorAPI(indicador='dolar') * 5.5)
    aux = {
        'precio1' : precio1,
        'precio2' : precio2,
        'precio3' : precio3,
        'precio4' : precio4,
    }
    return render(request, 'core/res_servicios.html', aux)

@login_required
def carrito(request):
    precio1 = round(miindicadorAPI(indicador='dolar') * 2.5)
    precio2 = round(miindicadorAPI(indicador='dolar') * 10)
    precio3 = round(miindicadorAPI(indicador='dolar') * 8.5)
    precio4 = round(miindicadorAPI(indicador='dolar') * 5.5)
    aux = {
        'precio1' : precio1,
        'precio2' : precio2,
        'precio3' : precio3,
        'precio4' : precio4,
    }
    return render(request, 'core/carrito.html', aux)

@login_required
def agregar_carrito(request, usuario, servicio):
    precio1 = round(miindicadorAPI(indicador='dolar') * 2.5)
    precio2 = round(miindicadorAPI(indicador='dolar') * 10)
    precio3 = round(miindicadorAPI(indicador='dolar') * 8.5)
    precio4 = round(miindicadorAPI(indicador='dolar') * 5.5)
    aux = {
        'precio1' : precio1,
        'precio2' : precio2,
        'precio3' : precio3,
        'precio4' : precio4,
    }
    if request.method == "POST":
        servicio_nombre = f'servicio_{servicio}'
        
        carrito_obj, created = Carrito.objects.get_or_create(usuario=usuario)
        
        setattr(carrito_obj, servicio_nombre, Carrito.SI)
        carrito_obj.actualizar_total()
        carrito_obj.save()

        return render(request, 'core/res_servicios.html', aux)
    
    return render(request, 'core/res_servicios.html')

@login_required
def eliminar_carrito(request, usuario, servicio):
    if request.method == "POST":
        servicio_nombre = f'servicio_{servicio}'
        
        carrito_obj, created = Carrito.objects.get_or_create(usuario=usuario)
        
        setattr(carrito_obj, servicio_nombre, Carrito.NO)
        carrito_obj.actualizar_total()
        carrito_obj.save()


        return render(request, 'core/res_servicios.html', {'carrito': carrito_obj})

    return render(request, 'core/res_servicios.html')

@login_required
def limpiar_carrito(request, usuario):
    if request.method == "POST":
        carrito_obj, created = Carrito.objects.get_or_create(usuario=usuario)
        
        # Cambiar el estado de todos los servicios a "NO"
        carrito_obj.servicio_1 = Carrito.NO
        carrito_obj.servicio_2 = Carrito.NO
        carrito_obj.servicio_3 = Carrito.NO
        carrito_obj.servicio_4 = Carrito.NO

        # Actualizar el total del carrito
        carrito_obj.actualizar_total()
        carrito_obj.save()

        return render(request, 'core/carrito.html', {'carrito': carrito_obj})

    return render(request, 'core/carrito.html')

@csrf_exempt
@login_required
def procesar_pago(request):
    if request.method == "POST":
        data = json.loads(request.body)
        payment_id = data.get('paymentID')
        payer_id = data.get('payerID')
        payment_token = data.get('paymentToken')
        payment_details = data.get('paymentDetails')

        # Guardar los datos del pago en el modelo Pago_reserva
        Pago_reserva.objects.create(
            usuario=request.user.username,
            id_pago=payment_id,
            id_pagador=payer_id,
            token_pago=payment_token,
            detalle_pago=payment_details
        )

        user = request.user

        user_info = {'user': user}

        carrito = Carrito.objects.filter(usuario=user_info['user']).first()

        servicios_list = []
        if carrito:
            if carrito.servicio_1 == Carrito.SI:
                servicios_list.append("Pruebas de diagnóstico")
            if carrito.servicio_2 == Carrito.SI:
                servicios_list.append("Mantención de Motores")
            if carrito.servicio_3 == Carrito.SI:
                servicios_list.append("Reemplazo de neumáticos")
            if carrito.servicio_4 == Carrito.SI:
                servicios_list.append("Cambio de aceite")

        servicios = ', '.join(servicios_list)
        nombre_apellido = f'{user.first_name} {user.last_name}'
        Reserva.objects.create(
            nombre_apellido= nombre_apellido,
            email_reserva=user.email,
            servicios=servicios,
        )

        # Limpiar el carrito del usuario
        if carrito:
            carrito.servicio_1 = Carrito.NO
            carrito.servicio_2 = Carrito.NO
            carrito.servicio_3 = Carrito.NO
            carrito.servicio_4 = Carrito.NO
            carrito.total_carrito = 0
            carrito.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failed'}, status=400)

@login_required
def historial_pago(request):
    user = request.user
    pagos = Pago_reserva.objects.filter(usuario=user.username)
    
    # Preparar los datos a mostrar en la plantilla
    pagos_info = []
    for pago in pagos:
        detalle_pago = pago.detalle_pago
        total = detalle_pago.get('transactions', [{}])[0].get('amount', {}).get('total', 'N/A')
        payer_info = detalle_pago.get('payer', {}).get('payer_info', {})
        nombre = payer_info.get('first_name', 'N/A') + ' ' + payer_info.get('last_name', 'N/A')
        email = payer_info.get('email', 'N/A')
        
        pagos_info.append({
            'id': pago.id,
            'usuario': pago.usuario,
            'id_pago': pago.id_pago,
            'fecha': pago.fecha,
            'total': total,
            'nombre': nombre,
            'email': email
        })
    
    aux = {
        'lista': pagos_info
    }

    return render(request, 'core/historial_pago.html', aux)

@login_required
def generar_pdf_voucher(request, id):
    user = request.user
    pago_info = Pago_reserva.objects.get(id=id, usuario=user.username)

    detalle_pago = pago_info.detalle_pago
    total = detalle_pago.get('transactions', [{}])[0].get('amount',{}).get('total', 'N/A')
    payer_info = detalle_pago.get('payer',{}).get('payer_info',{})
    email =payer_info.get('email', 'N/A')
    nombre = payer_info.get('first_name', 'N/A') + ' ' + payer_info.get('last_name', 'N/A') 
    id_cart_p = detalle_pago.get('cart', 'N/A')
    cod_pais = payer_info.get('country_code', 'N/A')
    pais = paisAPI(cod_pais)
    cod_postal = payer_info.get('shipping_address',{}).get('postal_code', 'N/A')


    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []


    story.append(Paragraph(f'ID Pago: {pago_info.id_pago}', styles['Title']))
    story.append(Paragraph(f'ID Pagador: {pago_info.id_pagador}', styles['BodyText']))
    story.append(Paragraph(f'TOKEN: {pago_info.token_pago}', styles['BodyText']))
    story.append(Paragraph(f'ID Carrito: {id_cart_p}', styles['BodyText']))
    story.append(Paragraph(f'Nombre: {nombre}', styles['BodyText']))
    story.append(Paragraph(f'Email: {email}', styles['BodyText']))
    story.append(Paragraph(f'Fecha Pago: {pago_info.fecha}', styles['BodyText']))
    story.append(Paragraph(f'Codigo Pais: {cod_pais}', styles['BodyText']))
    story.append(Paragraph(f'Pais: {pais}', styles['BodyText']))
    story.append(Paragraph(f'Codigo Postal: {cod_postal}', styles['BodyText']))
    story.append(Paragraph(f'Total: {total} USD', styles['BodyText']))

    doc.build(story)

    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="voucher_{pago_info.id}.pdf"'

    return response

def voucher(request, id):
    user = request.user
    pago_info = Pago_reserva.objects.get(id=id, usuario=user.username)

    detalle_pago = pago_info.detalle_pago
    total = detalle_pago.get('transactions', [{}])[0].get('amount',{}).get('total', 'N/A')
    payer_info = detalle_pago.get('payer',{}).get('payer_info',{})
    email =payer_info.get('email', 'N/A')
    nombre = payer_info.get('first_name', 'N/A') + ' ' + payer_info.get('last_name', 'N/A') 
    id_cart_p = detalle_pago.get('cart', 'N/A')
    cod_pais = payer_info.get('country_code', 'N/A')
    pais = paisAPI(cod_pais)
    cod_postal = payer_info.get('shipping_address',{}).get('postal_code', 'N/A')


    aux = {
        'id': pago_info.id,
        'usuario': pago_info.usuario,
        'id_pago': pago_info.id_pago,
        'id_token' : pago_info.token_pago,
        'fecha': pago_info.fecha,
        'nombre': nombre,
        'email': email,
        'id_carrito' : id_cart_p,
        'cod_pais' : cod_pais,
        'pais' : pais,
        'cod_postal' : cod_postal,
        'total': total
    }

    return render(request, 'core/voucher.html', aux)
