from django import template

register = template.Library()

@register.filter
def hash(h, key):
    return h[key]

@register.filter
def dict_has_key(h, key):
    return h.has_key(key)

@register.filter
def req2appr(o, prop):
    return o.prop

@register.simple_tag
def define(val=None):
    return val