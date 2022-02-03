import re
from textx import textx_isinstance
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q
from UksHub.apps.events.models import Comment
from UksHub.apps.advancedsearch.models import Query
from UksHub.apps.advancedsearch.constants import meta_model, is_values, sort_values, m_2_m


def get_artefact_content_type(type):
    return ContentType.objects.get(model=_get_is(type))


def _get_is(word):
    return is_values.get(word, None)


def _get_sort(word):
    return sort_values.get(word, None)


def _get_sv_condition(word):
    return m_2_m.get(word, None)


def _get_no_value(word):
    return m_2_m.get(word, None)


def map_query_to_filter(query):
    model = meta_model.model_from_str(re.sub(' +', ' ', query.strip()))
    filter = dict()
    match = list()
    sort = list()
    exclude = dict()
    annotate = dict()
    query = Query()
    for expression in model.expressions:
        if textx_isinstance(expression, meta_model['IsExpression']):
            value = expression.value.value
            if value in ['pr', 'issue']:
                query.entity.append(f'is:{value}')
                if 'polymorphic_ctype' in filter:
                    continue  # Implement multiple OR
                filter['polymorphic_ctype'] = get_artefact_content_type(value)
            elif value in ['open', 'closed']:
                query.state.append(f'is:{value}')
                if 'state' in filter:
                    continue  # Implement multiple OR
                filter['state'] = _get_is(value)
            else:
                query.match.append(f'is:{value}')

        elif textx_isinstance(expression, meta_model['SortExpression']):
            query.sort.append(f'sort:{expression.value.value}')
            value = _get_sort(expression.value.value)
            if value:
                if expression.value.value in ['comments-asc', 'comments-desc']:
                    annotate['comments_count'] = Count('event_set', filter=Q(
                        event_set__polymorphic_ctype=ContentType.objects.get_for_model(Comment)))
                sort.append(value)

        # Label specific
        elif textx_isinstance(expression, meta_model['ExcludingExpression']):
            query.exclude.append(
                f'-{expression.condition.value}:{expression.value.value}')

        # Label specific
        elif textx_isinstance(expression, meta_model['MultyValueExpression']):
            query.multi.append(
                f'{expression.condition.value}:{",".join(v.value for v in expression.value.values)}')

        elif textx_isinstance(expression, meta_model['SingleValueExpression']):
            # Check for quotes in expression, use value without them but have them in dispaly query again
            if textx_isinstance(expression.value, meta_model['QuotedValue']):
                value = expression.value.value.replace('"', '')
            else:
                value = expression.value.value

            # Same as on GH, match only last expression of same type, ignores all previous occurrences
            if expression.condition:
                condition = _get_sv_condition(expression.condition.value)
                if condition:
                    filter[condition] = value
                    setattr(query,
                            expression.condition.value,
                            [f'{expression.condition.value}:{expression.value.value}'])
            else:
                match.append(Q(name__contains=value) |
                             Q(message__message__contains=value))
                query.match.append('{}{}'.format(
                    f"{expression.condition.value}:" if expression.condition else "", expression.value.value))

        # Same as on GH, match only last expression of same type, ignores all previous occurrences
        elif textx_isinstance(expression, meta_model['NoEntityExpression']):
            value = expression.value.value
            m_2_m_value = _get_no_value(value)
            if m_2_m_value:
                filter[m_2_m_value] = None
                setattr(query, value, [f'no:{value}'])
            else:
                query.match.append(f'no:{value}')

        # RP only
        elif textx_isinstance(expression, meta_model['ReviewExpression']):
            query.review.append(
                f'{expression.condition.value}:{expression.value.value}')

    return filter, sort, exclude, annotate, match, query
