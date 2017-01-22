from django.template import Library

register = Library()

@register.simple_tag
def value(value):
    """
    Return value unless it's None in which case we return 'No Value Set'
    """
    if value == None or value == '':
        return 'No Value Set'
    else:
        return value
