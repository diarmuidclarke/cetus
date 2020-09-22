from django import template

register = template.Library()

@register.filter
def hash(h, key):
    return h[key]

@register.filter
def req2appr(o, prop):
    return o.prop
