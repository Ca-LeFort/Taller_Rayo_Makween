from rest_framework import serializers
from .models import *

class TipoServicioSerializers(serializers.ModelSerializer):
    class Meta:
        model = TipoServicio
        fields = '__all__'

class MecanicoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Mecanico
        fields = '__all__'

class ClienteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class TrabajoSerializers(serializers.ModelSerializer):
    tipo_servicio = TipoServicioSerializers(read_only=True)
    mecanico = MecanicoSerializers(read_only=True)
    cliente = ClienteSerializers(read_only=True)

    class Meta:
        model = Trabajo
        fields = '__all__'

class EstadoTrabajoSerializers(serializers.ModelSerializer):
    trabajo = TrabajoSerializers(read_only=True)

    class Meta:
        model = EstadoTrabajo
        fields = '__all__'

class TipoConsultaSerializers(serializers.ModelSerializer):
    class Meta:
        model = TipoConsulta
        fields = '__all__'

class ContactoSerializers(serializers.ModelSerializer):
    tipo_consulta = TipoConsultaSerializers(read_only=True)

    class Meta:
        model = Contacto
        fields = '__all__'

class ReservaSerializers(serializers.ModelSerializer):
    cliente = ClienteSerializers(read_only=True)
    mecanico = MecanicoSerializers(read_only=True)

    class Meta:
        model = Reserva
        fields = '__all__'

class PagoReservaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pago_reserva
        fields = '__all__'

class CarritoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Carrito
        fields = '__all__'


