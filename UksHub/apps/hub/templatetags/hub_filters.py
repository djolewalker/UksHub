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


@register.filter(name='cmt_msg')
def get_item(dictionary, key):
    return dictionary.get(key).message


@register.filter(name='cmt_time')
def get_item(dictionary, key):
    return dictionary.get(key).committed_datetime