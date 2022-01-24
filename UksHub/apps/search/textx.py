import re
from git import os
from textx import metamodel_from_file, textx_isinstance
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q
from UksHub.apps.core.enums import BASE_STATE
from UksHub.apps.events.models import Comment

from UksHub.apps.hub.models import Issue, PullRequest
from UksHub.apps.search.models import Query

module_dir = os.path.dirname(__file__)
_meta_model = metamodel_from_file(os.path.join(
    module_dir, 'search-metamodel.tx'), skipws=False, ws='\s')

is_values = {
    'open': BASE_STATE.OPEN.value,
    'closed': BASE_STATE.CLOSED.value,
    'pr': ContentType.objects.get_for_model(PullRequest),
    'issue': ContentType.objects.get_for_model(Issue),
}

sort_values = {
    'created-asc': 'created_at',
    'updated-asc': 'updated_at',
    'comments-asc': 'comments_count',
    'created-desc': '-created_at',
    'updated-desc': '-updated_at',
    'comments-desc': '-comments_count',
}

single_values = {
    'author': 'creator__username',
    'assignee': 'assignees__username'
}


def _get_is(word):
    return is_values.get(word, None)


def _get_sort(word):
    return sort_values.get(word, None)


def _get_sv(word):
    return single_values.get(word, None)


def map_query_to_filter(query):
    model = _meta_model.model_from_str(re.sub(' +', ' ', query.strip()))
    filter = dict()
    match = list()
    sort = list()
    exclude = dict()
    annotate = dict()
    query = Query()
    for expression in model.expressions:
        if textx_isinstance(expression, _meta_model['IsExpression']):
            if expression.value in ['pr', 'issue']:
                query.entity.append(f'is:{expression.value}')
                if 'polymorphic_ctype' in filter:
                    continue  # Implement multiple OR
                filter['polymorphic_ctype'] = _get_is(expression.value)
            elif expression.value in ['open', 'closed']:
                query.state.append(f'is:{expression.value}')
                if 'state' in filter:
                    continue  # Implement multiple OR
                filter['state'] = _get_is(expression.value)
            else:
                query.match.append(f'is:{expression.value}')

        elif textx_isinstance(expression, _meta_model['SortExpression']):
            query.sort.append(f'sort:{expression.value}')
            value = _get_sort(expression.value)
            if value:
                if expression.value in ['comments-asc', 'comments-desc']:
                    annotate['comments_count'] = Count('event_set', filter=Q(
                        event_set__polymorphic_ctype=ContentType.objects.get_for_model(Comment)))
                sort.append(value)

        elif textx_isinstance(expression, _meta_model['ExcludingExpression']):
            query.exclude.append(
                f'-{expression.condition.value}:{expression.value}')

        elif textx_isinstance(expression, _meta_model['MultyValueExpression']):
            query.multi.append(
                f'{expression.condition.value}:{",".join(v.value for v in expression.value.values)}')

        elif textx_isinstance(expression, _meta_model['SingleValueExpression']):
            if expression.condition:
                condition = _get_sv(expression.condition.value)
                if condition:
                    filter[condition] = expression.value.value
                    setattr(query,
                            expression.condition.value,
                            [
                                *getattr(query, expression.condition.value),
                                f'{expression.condition.value}:{expression.value.value}'
                            ])
                    continue
            else:
                match.append(Q(name__contains=expression.value.value) |
                             Q(message__message__contains=expression.value.value))

            query.match.append('{}{}'.format(
                f"{expression.condition.value}:" if expression.condition else "", expression.value.value))

        elif textx_isinstance(expression, _meta_model['NoEntityExpression']):
            query.no.append(f'no:{expression.value}')

        elif textx_isinstance(expression, _meta_model['ReviewExpression']):
            query.review.append(
                f'{expression.condition.value}:{expression.value}')

    return filter, sort, exclude, annotate, match, query
