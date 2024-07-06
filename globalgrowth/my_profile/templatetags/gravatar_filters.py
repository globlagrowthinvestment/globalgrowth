import hashlib
from django import template

register = template.Library()

@register.filter
def gravatar_url(email):
    email = email.lower().encode('utf-8')
    return hashlib.md5(email).hexdigest()