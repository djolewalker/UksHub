import os
from textx import metamodel_from_file
from UksHub.apps.core.enums import BASE_STATE

module_dir = os.path.dirname(__file__)
meta_model = metamodel_from_file(os.path.join(
    module_dir, 'search-metamodel.tx'), skipws=False, ws='\s')

is_values = {
    'open': BASE_STATE.OPEN.value,
    'closed': BASE_STATE.CLOSED.value,
    'pr': 'PullRequest',
    'issue': 'Issue',
}


sort_values = {
    'created-asc': 'created_at',
    'updated-asc': 'updated_at',
    'comments-asc': 'comments_count',
    'created-desc': '-created_at',
    'updated-desc': '-updated_at',
    'comments-desc': '-comments_count',
}

m_2_m = {
    'author': 'creator__username',
    'assignee': 'assignees__username',
    'milestone': '',
    'project': '',
    'label': ''
}
