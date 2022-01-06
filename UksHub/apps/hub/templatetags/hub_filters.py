from django import template

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
