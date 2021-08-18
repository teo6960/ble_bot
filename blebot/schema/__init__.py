from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.dialects.postgresql import ARRAY

modmethods = ['add', 'clear', 'difference_update', 'discard',
              'intersection_update', 'pop', 'remove',
              'symmetric_difference_update', 'update',
              '__ior__', '__iand__', '__isub__', '__ixor__']

class MutableSet(Mutable, set):
    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, cls):
            return cls(value)
        else:
            return value

def _make_mm(mmname):
    def mm(self, *args, **kwargs):
        try:
            retval = getattr(set, mmname)(self, *args, **kwargs)
        finally:
            self.changed()
        return retval
    return mm

for m in modmethods:
    setattr(MutableSet, m, _make_mm(m))

del modmethods, _make_mm

def ArraySet(_type, dimensions=1):
    return MutableSet.as_mutable(ARRAY(_type, dimensions=dimensions))
