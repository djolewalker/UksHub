from django.core.validators import RegexValidator

path_validator = RegexValidator(r'^[0-9a-zA-Z_-]*$', 'Only alphanumeric and - _ characters are allowed.')