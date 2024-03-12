
class BaseEntity:

    def _gather_attrs(self):
        return ",".join("{} = {}".format(k, getattr(self, k)) for k in self.__dict__.keys())

    def __str__(self):
        return "[{}:{}]".format(self.__class__.__name__, self._gather_attrs())  