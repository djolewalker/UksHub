from enum import Enum

class BASE_STATE(Enum):
    OPEN = 1
    CLOSED = 2
    MERGED = 3

class REVIEW_STATE(Enum):
    COMMENT = 1
    APPROVE = 2
    REQUEST_CHANGE = 3


class CHECK_STATE(Enum):
    STARTED = 1
    SUCCESSFUL = 2
    FAILED = 3