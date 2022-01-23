from django import template
from django.contrib.contenttypes.models import ContentType
import base64
import hashlib

from UksHub.apps.core.enums import BASE_STATE
from UksHub.apps.hub.models import Issue, PullRequest

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
def get_msg(dictionary, key):
    return dictionary.get(key).message


@register.filter(name='cmt_time')
def get_time(dictionary, key):
    return dictionary.get(key).committed_datetime


@register.filter(name='decode')
def decode(text, format):
    return text.decode(format)


@register.filter(name='base64')
def encode_base64(text):
    return base64.b64encode(text)

    
@register.filter(name='split')
def split_str(text, chr):
    return text.split(chr)


@register.filter(name='count')
def count_str(text, chr):
    return text.count(chr)


@register.filter(name='isissue')
def is_issue(entity):
    return isinstance(entity, Issue)


@register.filter(name='ispr')
def is_pr(entity):
    return isinstance(entity, PullRequest)


@register.filter(name='issuecount')
def count_issue(repo):
    return repo.artefact_set.filter(polymorphic_ctype=ContentType.objects.get_for_model(Issue), state=BASE_STATE.OPEN.value).count()


@register.filter(name='prcount')
def count_pr(repo):
    return repo.artefact_set.filter(polymorphic_ctype=ContentType.objects.get_for_model(PullRequest), state=BASE_STATE.OPEN.value).count()


@register.filter(name='opencount')
def count_open(artefacts):
    return artefacts.filter(state=BASE_STATE.OPEN.value).count()


@register.filter(name='closedcount')
def count_closed(artefacts):
    return artefacts.filter(state=BASE_STATE.CLOSED.value).count()
