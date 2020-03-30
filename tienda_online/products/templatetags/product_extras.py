from django import template

#cuando quiera implementar filtros que django no provee los tengo que generar de esta manera.
#primero creo la carpeta templatetags, dentro el archivo __init__.py y luego todos los filtros que quiera

register = template.Library()


@register.filter()
def price_format(value):
    return '${0:.2f}'.format(value)