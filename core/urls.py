from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('tiposervicio', TipoServicioViewset)
router.register('mecanico', MecanicoViewset)
router.register('cliente', ClienteViewset)
router.register('trabajo', TrabajoViewset)
router.register('estadotrabajo', EstadoTrabajoViewset)
router.register('tipoconsultas', TipoConsultasViewset)
router.register('contacto', ContactoViewset)
router.register('reserva', ReservaViewset)
router.register('pago_reserva', PagoReservaViewset)
router.register('carrito', CarritoViewset)

urlpatterns = [
    path('', index, name="index"),
    path('nosotros/', nosotros, name="nosotros"),
    path('contacto/', contacto, name="contacto"),
    path('mecanicos/', mecanicos, name="mecanicos"),
    path('register/', register, name="register"),
    path('login/', login, name="login"),
    path('logout/', logout_view, name="logout"),
    path('galeria/', galeria, name="galeria"),
    path('servicios/', servicios, name="servicios"),
    path('404/', pagina_404, name="404"),
    path('mecanicos/mecanicoadd/', mecanicoadd, name="mecanicoadd"),
    path('mecanicos/mecanicolistar/', mecanicos, name="mecanicolistar"),
    path('mecanicos/mecanicoupdate/<id>/', mecanicoupdate, name="mecanicoupdate"),
    path('mecanicos/mecanicodelete/<id>/', mecanicodelete, name="mecanicodelete"),
    path('mecanicos/trabajoadd/', trabajoadd, name="trabajoadd"),
    path('mecanicos/trabajolistar/', trabajos, name="trabajolistar"),
    path('mecanicos/trabajoupdate/<id>/', trabajoupdate, name="trabajoupdate"),
    path('mecanicos/listarconsultas/', listarconsultas, name="listarconsultas"),
    path('mecanicos/listarreservas/', listarreservas, name="listarreservas"),
    path('mecanicos/reservaupdate/<id>/', reservaupdate, name="reservaupdate"),
    path('trabajo/<id>/', trabajo, name="trabajo"),
    path('reserva/', reserva, name="reserva"),
    path('categoria_trabajo/<int:id>/', categoria_trabajo, name="categoria_trabajo"),
    path('mecanico_trabajo/<id>/', mecanico_trabajo, name="mecanico_trabajo"),
    path('buscar/', buscador, name='buscador'),
    path('clientes/', clientes, name='clientes'),
    path('account_locked/', account_locked, name='account_locked'),
    path('res_servicios/', res_servicios, name="res_servicios"),
    path('agregar_carrito/<str:usuario>/<int:servicio>/', agregar_carrito, name='agregar_carrito'),
    path('eliminar_carrito/<str:usuario>/<int:servicio>/', eliminar_carrito, name='eliminar_carrito'),
    path('limpiar_carrito/<str:usuario>/', limpiar_carrito, name='limpiar_carrito'),
    path('carrito/', carrito, name="carrito"),
    path('procesar_pago/', procesar_pago, name="procesar_pago"),
    path('historial_pago/', historial_pago, name="historial_pago"),
    path('generar_pdf_voucher/<int:id>/',generar_pdf_voucher, name='generar_pdf_voucher'),
    path('voucher/<id>/', voucher, name="voucher"),
    # APIs
    path('api/', include(router.urls)),
    #path('mecanicosapi/', mecanicosapi, name="mecanicosapi"),
    #path('mecanicodetalle/<id>/', mecanicodetalle, name="mecanicodetalle"),
]
