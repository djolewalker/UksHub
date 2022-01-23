from copy import copy


class Query:
    def __init__(self):
        self.entity = []
        self.state = []
        self.sort = []
        self.exclude = []
        self.multi = []
        self.match = []
        self.no = []
        self.review = []
        pass

    def __str__(self):
        return " ".join([*self.entity, *self.state, *self.sort, *self.exclude, *self.multi, *self.match, *self.no, *self.review])

    def set_entity(self, entity):
        e = copy(self)
        e.entity = _get_as_list(entity)
        return e

    def set_state(self, state):
        e = copy(self)
        e.state = _get_as_list(state)
        return e

    def set_sort(self, sort):
        e = copy(self)
        e.sort = _get_as_list(sort)
        return e

    def set_exclude(self, exclude):
        e = copy(self)
        e.exclude = _get_as_list(exclude)
        return e

    def set_multi(self, multi):
        e = copy(self)
        e.multi = _get_as_list(multi)
        return e

    def set_match(self, match):
        e = copy(self)
        e.match = _get_as_list(match)
        return e

    def set_no(self, no):
        e = copy(self)
        e.no = _get_as_list(no)
        return e

    def set_review(self, review):
        e = copy(self)
        e.review = _get_as_list(review)
        return e


def _get_as_list(value):
    return [*value] if isinstance(value, list) else [value]
