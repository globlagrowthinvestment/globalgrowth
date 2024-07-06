from django import template
import hashlib

register = template.Library()
register.filter('gravatar_url', lambda u: hashlib.md5(u.lower().encode('utf8')).hexdigest())