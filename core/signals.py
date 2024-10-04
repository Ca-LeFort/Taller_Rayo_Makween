from django.db.models.signals import post_save
from django.dispatch import receiver
import cloudinary.uploader
from .models import *

@receiver(post_save, sender=Trabajo)
def rename_cloudinary_image(sender, instance, **kwargs):
    if instance.foto:

        if hasattr(instance.foto, 'url'):
            ext = instance.foto.url.split('.')[-1]
            new_public_id = f'trabajos/Imagen_{instance.pk}' 
            current_public_id = instance.foto.public_id

            if current_public_id != new_public_id:
                try:
                    cloudinary.uploader.rename(current_public_id, new_public_id)
                except cloudinary.api.Error as e:
                    print(f"Error al renombrar imagen en Cloudinary: {str(e)}")

                instance.foto = new_public_id + '.' + ext
                instance.save()
        else:
            print(f"La foto no es un objeto de Cloudinary: {instance.foto}")


@receiver(post_save, sender=Mecanico)
def rename_cloudinary_image_mecanico(sender, instance, **kwargs):
    if instance.foto_mecanico:

        if hasattr(instance.foto_mecanico, 'url'):
            ext = instance.foto_mecanico.url.split('.')[-1]
            new_public_id = 'mecanicos/Imagen {}'.format(instance.pk)
            current_public_id = instance.foto_mecanico.public_id


            if current_public_id != new_public_id:
                cloudinary.uploader.rename(current_public_id, new_public_id)
                instance.foto_mecanico = new_public_id + '.' + ext
                instance.save()
        else:
            print(f"Foto is not a Cloudinary object: {instance.foto_mecanico}")