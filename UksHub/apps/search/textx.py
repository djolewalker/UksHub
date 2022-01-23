from textx import metamodel_from_file, textx_isinstance
from django.contrib.contenttypes.models import ContentType
from UksHub.apps.core.enums import BASE_STATE

from UksHub.apps.hub.models import Issue, PullRequest


_meta_model = metamodel_from_file('search-metamodel.tx', skipws=False, ws='\s')


def map_query_to_filter(query):
    model = _meta_model.model_from_str(query)
    filter = dict()
    sort = None
    exclude = dict()
    for expression in model.expression:
        if textx_isinstance(expression, _meta_model['IsExpression']):
            if expression.value in ['pr', 'issue']:
                if 'polymorphic_ctype' in filter: continue
                filter['polymorphic_ctype']=ContentType.objects.get_for_model(PullRequest if expression.value == 'pr' else Issue)
            else:
                filter['state']=BASE_STATE.OPEN.value if expression.value == 'open' else BASE_STATE.CLOSED.value
        elif textx_isinstance(expression, _meta_model['SortExpression']):
            pass
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