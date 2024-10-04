from django.contrib import admin
from .models import *
from admin_confirm import AdminConfirmMixin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.forms import AuthenticationForm

class TipoServicioModelAdmin(AdminConfirmMixin, ModelAdmin):
        confirm_change = True
        confirmation_fields = ['descripcion']

class TrabajoModelAdmin(AdminConfirmMixin, ModelAdmin):
        confirm_change = True
        confirmation_fields = ['nombre_trabajo', 'diagnostico', 'fecha', 'mecanico', 'materiales', 'foto', 'servicio', 'estado_publicacion', 'comentario_admin', 'cliente']

class ClienteModelAdmin(AdminConfirmMixin, ModelAdmin):
        confirm_change = True
        confirmation_fields = ['nombre_cliente', 'apellido_cliente', 'correo_cliente', 'cant_mantenciones_cli']

class TipoConsultaAdmin(AdminConfirmMixin, ModelAdmin):
        confirm_change = True
        confirmation_fields = ['descripcion']

class ContactoModelAdmin(AdminConfirmMixin, ModelAdmin):
        confirm_change = True
        confirmation_fields = ['nombre_apellido', 'email_contacto', 'telefono', 'consulta', 'info_adicional']

class MecanicoModelAdmin(AdminConfirmMixin, ModelAdmin):
        confirm_change = True
        confirmation_fields = ['nombre_mecanico', 'apellido_mecanico', 'correo_mecanico', 'password_mecanico', 'foto_mecanico', 'cant_mantenciones_mec']

class CarritoModelAdmin(AdminConfirmMixin, ModelAdmin):
        confirm_change = True
        confirmation_fields = ['usuario', 'servicio_1', 'servicio_2', 'servicio_3', 'servicio_4', 'total_carrito']

class PagoReservaModelAdmin(AdminConfirmMixin, ModelAdmin):
        confirm_change = True
        confirmation_fields = ['usuario', 'id_pago', 'id_pagador', 'token_pago', 'detalle_pago']

# Register your models here.
admin.site.register(TipoServicio, TipoServicioModelAdmin)
admin.site.register(Trabajo, TrabajoModelAdmin)
admin.site.register(Cliente, ClienteModelAdmin)
admin.site.register(TipoConsulta, TipoConsultaAdmin)
admin.site.register(Contacto, ContactoModelAdmin)
admin.site.register(Mecanico, MecanicoModelAdmin)
admin.site.register(Reserva)
admin.site.register(Carrito, CarritoModelAdmin)
admin.site.register(Pago_reserva, PagoReservaModelAdmin)
