from django.db import models
from django.utils.translation import ugettext_lazy as _


class BooleanIntField(models.BooleanField):
    description = _('Boolean represented as int4')

    def __init__(self, *args, **kwargs):
        super(BooleanIntField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'PositiveIntegerField'

    def to_python(self, value):
        if isinstance(value, int):
            return value != 0
        return super(BooleanIntField, self).to_python(value)

    def get_prep_value(self, value):
        value = super(BooleanIntField, self).get_prep_value(value)
        return None if value is None else int(value)


class BooleanSmallIntField(BooleanIntField):
    description = _('Boolean represented as int2')

    def get_internal_type(self):
        return 'PositiveSmallIntegerField'
