import re
from git import os
from textx import metamodel_from_file, textx_isinstance
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q
from UksHub.apps.core.enums import BASE_STATE
from UksHub.apps.events.models import Comment, UserAssignment

from UksHub.apps.hub.models import Issue, PullRequest

module_dir = os.path.dirname(__file__)
_meta_model = metamodel_from_file(os.path.join(module_dir, 'search-metamodel.tx'), skipws=False, ws='\s')


def map_query_to_filter(query):
    model = _meta_model.model_from_str(query)
    filter = dict()
    sort = list()
    exclude = dict()
    annotate = dict()
    for expression in model.expressions:
        if textx_isinstance(expression, _meta_model['IsExpression']):
            if expression.value in ['pr', 'issue']:
                if 'polymorphic_ctype' in filter: continue
                filter['polymorphic_ctype']=ContentType.objects.get_for_model(PullRequest if expression.value == 'pr' else Issue)
            else:
                if 'state' in filter: continue
                filter['state']=BASE_STATE.OPEN.value if expression.value == 'open' else BASE_STATE.CLOSED.value

        elif textx_isinstance(expression, _meta_model['SortExpression']):
            if expression.value:
                direction = '-' if expression.value.direction == 'desc' else ''
                if expression.value.property == 'comments':
                    property = 'comments_count'
                    annotate[property]=Count('event_set', filter=Q(event_set__polymorphic_ctype=ContentType.objects.get_for_model(Comment)))
                else:
                    property = 'created_at' if expression.value.property == 'created' else 'updated_at'
                sort.append(f'{direction}{property}')

        elif textx_isinstance(expression, _meta_model['ExcludingExpression']):
            pass
        elif textx_isinstance(expression, _meta_model['MultyValueExpression']):
            pass
        elif textx_isinstance(expression, _meta_model['SingleValueExpression']):
            pass
        elif textx_isinstance(expression, _meta_model['NoEntityExpression']):
            pass
        elif textx_isinstance(expression, _meta_model['ReviewExpression']):
            pass

    return filter, sort, exclude, annotate