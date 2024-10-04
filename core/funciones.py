import requests

def upload_to_mecanicos(instance, filename):
    ext = filename.split('.')[-1]
    if instance.pk:
        return 'mecanicos/Imagen {}.{}'.format(instance.pk, ext)
    else:
        count = instance.__class__.objects.count() + 1
        return 'mecanicos/Imagen {}.{}'.format(count, ext)

def upload_to_trabajos(instance, filename):
    ext = filename.split('.')[-1]
    if instance.pk:
        return 'trabajos/Imagen {}.{}'.format(instance.pk, ext)
    else:
        count = instance.__class__.objects.count() + 1
        return 'trabajos/Imagen {}.{}'.format(count, ext)
    
def miindicadorAPI(indicador):
    response = requests.get(f'https://mindicador.cl/api/{indicador}/')
    moneda = response.json()
    valor = moneda.get('serie', [{}])[0].get('valor')

    return valor

def paisAPI(code):
    response = requests.get('https://country.io/names.json')
    paises = response.json()
    nom_pais = paises.get(code)

    return nom_pais