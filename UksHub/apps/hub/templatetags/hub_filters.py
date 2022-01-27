from django import template
from django.contrib.contenttypes.models import ContentType
from base64 import b64encode
import hashlib

from UksHub.apps.core.enums import BASE_STATE
from UksHub.apps.hub.models import Issue, PullRequest

register = template.Library()


@register.filter(name='hash')
def hash(text):
    return hashlib.sha1(text.encode('utf8')).hexdigest()


@register.filter(name='cmt_msg')
def get_msg(dictionary, key):
    return dictionary.get(key).message


@register.filter(name='cmt_id')
def get_id(dictionary, key):
    return dictionary.get(key).binsha


@register.filter(name='cmt_time')
def get_time(dictionary, key):
    return dictionary.get(key).committed_datetime


@register.filter(name='diff_inserted')
def diff_inserted(dictionary, key):
    return dictionary.get(key).get('insertions')


@register.filter(name='diff_deleted')
def diff_deleted(dictionary, key):
    return dictionary.get(key).get('deletions')


@register.filter(name='decode')
def decode(text, format):
    return text.decode(format)


@register.filter(name='base64')
def encode_base64(text):
    return b64encode(text)


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


@register.filter(name='queryinclude')
def query_include(query, word):
    return query == word or query.startswith(f'{word} ') or query.endswith(f' {word}') or f' {word} ' in query


@register.filter(name='userordefault')
def user_or_default(repo, actor):
    try:
        user = repo.contributors.get(email=actor.email)
        return user.username if user else None
    except:
        return None
