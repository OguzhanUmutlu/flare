from __future__ import annotations

from .nbt import nbt


class _Storage:
    def __getattr__(self, name):
        return nbt(addr=f"storage {name}", datatype=None)

    def __setattr__(self, name, value):
        target = getattr(self, name)
        target[:] = value

    def __getitem__(self, item):
        return nbt(addr=f"storage {item}", datatype=None)

    def __setitem__(self, key, value):
        target = self[key]
        target[:] = value
