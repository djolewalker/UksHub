from django import template
import hashlib

register = template.Library()

@register.filter(name='initials')
def initials(fullname):
    xs = (fullname)
    name_list = xs.split()
    initials = ""
    for name in name_list:
        initials += name[0].upper()
        if len(initials) == 2:
            return initials
    return initials

@register.filter(name='hash')
def hash(text):
    return hashlib.sha1(text.encode('utf8')).hexdigest()


