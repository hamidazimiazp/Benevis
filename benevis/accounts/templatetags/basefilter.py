from django import template
register = template.Library()

@register.filter(name = 'time_format')
def time_format(value):
    return "{}".format(value.strftime("%Y-%m-%d %H:%M:%S %p"))