from __future__ import annotations

import inspect
from abc import ABC


def nostack(func):
    return func


def lazify(temp="!temp", datatype=None, self=True, copy=None):
    from .. import context as ctx
    def decorator(func):
        def wrapper(*args, **kwargs):
            if self is True:
                if not args:
                    raise TypeError(
                        f"{func.__name__}() missing 1 required positional argument: 'self'"
                    )
                obj_or_arg = args[0]

                def eval_func(dest, **eval_kwargs):
                    merged_kwargs = {**kwargs, **eval_kwargs}
                    return func(*args, dest=dest, **merged_kwargs)

                def alloc_temp():
                    if callable(temp):
                        if len(inspect.signature(temp).parameters) == 1:
                            dest = temp(obj_or_arg)
                        else:
                            dest = temp()
                    else:
                        dest = obj_or_arg._alloc_temp(prefix=temp)

                    if datatype is not None and hasattr(dest, "_type"):
                        dest._type = datatype
                    return dest

                def make_copy(varid):
                    if copy is not None:
                        return copy(obj_or_arg, varid)
                    if hasattr(obj_or_arg, "__icopy__"):
                        if (
                                datatype is None
                                or getattr(obj_or_arg, "_type", None) == datatype
                        ):
                            return obj_or_arg.__icopy__(varid)
                    t = alloc_temp()
                    if hasattr(t, "_parse_addr"):
                        t._parse_addr(f"storage {ctx._current_namespace}:vars {varid}")
                    else:
                        t._addr = f"storage {ctx._current_namespace}:vars {varid}"
                    return t

                return obj_or_arg._lazify(
                    eval_func,
                    alloc_temp,
                    make_copy,
                    op_name=func.__name__,
                    op_args=(args, kwargs),
                )
            else:
                def eval_func(dest, **eval_kwargs):
                    merged_kwargs = {**kwargs, **eval_kwargs}
                    return func(*args, dest=dest, **merged_kwargs)

                def alloc_temp():
                    nonlocal ctx

                    if callable(temp):
                        dest = temp()
                    else:
                        if isinstance(self, type) and issubclass(self, FlareValue):
                            dest = self(
                                addr=f"storage flare:temp {temp}_{ctx.next_temp_id()}"
                            )
                        else:
                            dest = nbt(
                                addr=f"storage flare:temp {temp}_{ctx.next_temp_id()}"
                            )
                    if datatype is not None and hasattr(dest, "_type"):
                        dest._type = datatype
                    return dest

                def make_copy(varid):
                    if copy is not None:
                        return copy(varid)
                    t = alloc_temp()
                    if hasattr(t, "_parse_addr"):
                        t._parse_addr(f"storage {ctx._current_namespace}:vars {varid}")
                    else:
                        t._addr = f"storage {ctx._current_namespace}:vars {varid}"
                    return t

                return LazyOp(
                    None,
                    eval_func,
                    alloc_temp,
                    make_copy,
                    op_name=func.__name__,
                    op_args=(args, kwargs),
                )

        return wrapper

    return decorator


class FlareValue(ABC):
    def __iset__(self, other):
        raise NotImplementedError()

    def __setitem__(self, key, value):
        if (
                isinstance(key, slice)
                and key.start is None
                and key.stop is None
                and key.step is None
        ):
            self.__iset__(value)
            return
        raise TypeError(
            f"'{type(self).__name__}' object does not support item assignment"
        )

    def _alloc_temp(self, prefix="!temp"):
        raise NotImplementedError(
            f"'{type(self).__name__}' does not implement _alloc_temp()"
        )

    def _compile_into(self, dest):
        raise NotImplementedError()

    def _lazify(
            self, eval_fn, alloc_temp_fn=None, make_copy_fn=None, op_name=None, op_args=None
    ):
        return LazyOp(
            self, eval_fn, alloc_temp_fn, make_copy_fn, op_name=op_name, op_args=op_args
        )

    def _best_leaf(self):
        return self._alloc_temp()

    def __branch__(self, invert=False):
        raise NotImplementedError()

    def __rin__(self, container):
        from .score import score
        from .. import context as ctx
        from ..context import _runcmd
        from ..compiler import _flatten_and

        if isinstance(container, (list, tuple, set)):
            if not container:
                return False

            dest = score(addr=f"!in_{ctx.next_temp_id()}")
            _runcmd(f"scoreboard players set {addr(dest)} 0")

            for item in container:
                cond = (self == item)
                if isinstance(cond, bool):
                    if cond:
                        _runcmd(f"scoreboard players set {addr(dest)} 1")
                        break
                    continue

                conds = _flatten_and(cond)
                _runcmd(
                    f"execute if score {addr(dest)} matches 0 {' '.join(conds)} run scoreboard players set {addr(dest)} 1")

            return dest == 1
        return NotImplemented

    def __add__(self, other):
        return BinaryOp(self, other, "add")

    def __radd__(self, other):
        return BinaryOp(other, self, "add")

    def __sub__(self, other):
        return BinaryOp(self, other, "sub")

    def __rsub__(self, other):
        return BinaryOp(other, self, "sub")

    def __mul__(self, other):
        return BinaryOp(self, other, "mul")

    def __rmul__(self, other):
        return BinaryOp(other, self, "mul")

    def __idiv__(self, other):
        raise NotImplementedError()

    def __itruediv__(self, other):
        return self.__idiv__(other)

    def __iadd__(self, other):
        raise NotImplementedError()

    def __isub__(self, other):
        raise NotImplementedError()

    def __imul__(self, other):
        raise NotImplementedError()

    def __imod__(self, other):
        raise NotImplementedError()

    def __ineg__(self):
        raise NotImplementedError()

    def __inot__(self):
        raise NotImplementedError()

    def __neg__(self):
        return UnaryOp(self, "neg")

    def __pos__(self):
        return self

    def __eq__(self, other):
        return BinaryOp(self, other, "eq")

    def __ne__(self, other):
        return BinaryOp(self, other, "ne")

    def __lt__(self, other):
        return BinaryOp(self, other, "lt")

    def __le__(self, other):
        return BinaryOp(self, other, "le")

    def __gt__(self, other):
        return BinaryOp(self, other, "gt")

    def __ge__(self, other):
        return BinaryOp(self, other, "ge")

    def __and__(self, other):
        return BinaryOp(self, other, "and")

    def __or__(self, other):
        return BinaryOp(self, other, "or")

    def __invert__(self):
        return UnaryOp(self, "not")

    def __truediv__(self, other):
        return BinaryOp(self, other, "truediv")

    def __rtruediv__(self, other):
        return BinaryOp(other, self, "truediv")

    def __mod__(self, other):
        return BinaryOp(self, other, "mod")

    def __rmod__(self, other):
        return BinaryOp(other, self, "mod")

    def __bool__(self):
        raise TypeError(
            "Flare variables cannot be evaluated as python booleans. Are you using an 'if' statement or 'in' operator outside of a Flare function (@export)?"
        )

    def __implicit__(self, target_types):
        raise NotImplementedError()

    def _try_binary(self, fn, op, other, possibilities=None):
        from .. import context as ctx

        if possibilities is None:
            possibilities = (type(self),)

        if isinstance(other, LazyOp):
            t = type(self)(addr=f"!lazy{ctx.next_temp_id()}")
            other._compile_into(t)
            other = t

        if not isinstance(other, possibilities):
            if type(other) in getattr(type(self), "_implements_set", tuple()):
                return getattr(self, fn)(type(self)(other))

            if fn == "__iset__":
                if hasattr(other, "__implicit__"):
                    return getattr(self, fn)(other.__implicit__(possibilities))
            elif fn.startswith("__i"):
                r_fn = f"__ri{fn[3:]}"
                if hasattr(other, r_fn):
                    res = getattr(other, r_fn)(self)
                    if res is not NotImplemented:
                        return getattr(self, "__iset__")(res)

            if hasattr(other, "__implicit__"):
                return getattr(self, fn)(other.__implicit__(possibilities))

        raise UnsupportedOperandError(self, op, other)


class BinaryOp(FlareValue):
    _implements_set = tuple()

    def __init__(self, left, right, op: str):
        self.left = left
        self.right = right
        self.op = op

    def _best_leaf(self):
        def get_priority(leaf):
            if hasattr(leaf, "_type_priority"):
                return leaf._type_priority()
            if isinstance(leaf, FlareValue):
                return 0
            return -999999

        def traverse(node):
            if isinstance(node, BinaryOp):
                left_leaf = traverse(node.left)
                right_leaf = traverse(node.right)
                if get_priority(left_leaf) >= get_priority(right_leaf):
                    return left_leaf
                else:
                    return right_leaf
            elif isinstance(node, UnaryOp):
                return traverse(node.operand)
            elif isinstance(node, LazyOp):
                return traverse(node._best_leaf())
            else:
                return node

        return traverse(self)

    def _alloc_temp(self, prefix="!temp", like=None):
        if like is not None:
            return like._alloc_temp(prefix=prefix)
        return self._best_leaf()._alloc_temp(prefix=prefix)

    def _compile_into(self, dest):
        if self.op in ("eq", "ne", "lt", "le", "gt", "ge", "and", "or", "not"):
            raise TypeError("Logical/Relational operators cannot be assigned directly.")
        iop = f"__i{self.op}__"

        left_node = self.left
        right_node = self.right

        if self.op in ("add", "mul"):

            def get_priority(node):
                if hasattr(node, "_best_leaf"):
                    node = node._best_leaf()
                if hasattr(node, "_type_priority"):
                    return node._type_priority()
                if isinstance(node, FlareValue):
                    return 0
                return -999999

            if get_priority(right_node) > get_priority(left_node):
                left_node, right_node = right_node, left_node

        if isinstance(left_node, (BinaryOp, UnaryOp, LazyOp, MathOp)):
            left_node._compile_into(dest)
        else:
            dest[:] = left_node
        if isinstance(right_node, (BinaryOp, UnaryOp, LazyOp, MathOp)):
            temp = self._alloc_temp(dest)
            right_node._compile_into(temp)
            getattr(dest, iop)(temp)
        else:
            getattr(dest, iop)(right_node)
        return dest

    def __icopy__(self, varid: str, is_recursive: bool = False):
        leaf = self._best_leaf()
        dest = leaf._create_var(varid)
        self._compile_into(dest)
        return dest

    def __branch__(self, invert=False):
        from ..compiler import _flatten_and, _compile_relational, _eval_to_bool_score

        if self.op == "and" and not invert:
            return _flatten_and(self.left, invert) + _flatten_and(self.right, invert)
        if self.op == "or" and invert:
            return _flatten_and(self.left, invert) + _flatten_and(self.right, invert)
        if self.op in ("eq", "ne", "lt", "le", "gt", "ge"):
            return [_compile_relational(self, invert)]

        dest = _eval_to_bool_score(self)
        keyword = "unless" if invert else "if"
        return [f"{keyword} score {addr(dest)} matches 1"]

    def __bool__(self):
        raise TypeError(
            "Flare variables cannot be evaluated as python booleans. Are you using an 'if' statement or 'in' operator outside of a Flare function (@export)?"
        )


class UnaryOp(FlareValue):
    def __init__(self, operand, op: str):
        self.operand = operand
        self.op = op

    def _best_leaf(self):
        def get_priority(leaf):
            if hasattr(leaf, "_type_priority"):
                return leaf._type_priority()
            if isinstance(leaf, FlareValue):
                return 0
            return -999999

        def traverse(node):
            if isinstance(node, BinaryOp):
                left_leaf = traverse(node.left)
                right_leaf = traverse(node.right)
                if get_priority(left_leaf) >= get_priority(right_leaf):
                    return left_leaf
                else:
                    return right_leaf
            elif isinstance(node, UnaryOp):
                return traverse(node.operand)
            else:
                return node

        return traverse(self)

    def _alloc_temp(self, prefix="!temp", like=None):
        return like._alloc_temp(prefix=prefix)

    def _compile_into(self, dest):
        if self.op in ("not",):
            raise TypeError("Logical operators cannot be assigned directly.")
        iop = f"__i{self.op}__"
        if isinstance(self.operand, (BinaryOp, UnaryOp)):
            self.operand._compile_into(dest)
        else:
            dest[:] = self.operand
        if hasattr(dest, iop):
            getattr(dest, iop)()
        elif self.op == "neg":
            dest *= -1
        else:
            raise TypeError(f"Operand does not support unary {self.op}")
        return dest

    def __icopy__(self, varid: str, is_recursive: bool = False):
        leaf = self._best_leaf()
        dest = leaf._create_var(varid)
        self._compile_into(dest)
        return dest

    def __branch__(self, invert=False):
        from ..compiler import _flatten_and, _eval_to_bool_score

        if self.op == "not":
            return _flatten_and(self.operand, not invert)
        if self.op == "neg":
            return BinaryOp(self, 0, "ne").__branch__(invert)

        dest = _eval_to_bool_score(self)
        keyword = "unless" if invert else "if"
        return [f"{keyword} score {addr(dest)} matches 1"]

    def __neg__(self):
        if self.op == "neg":
            return self.operand
        return UnaryOp(self, "neg")

    def __bool__(self):
        raise TypeError(
            "Flare variables cannot be evaluated as python booleans. Are you using an 'if' statement or 'in' operator outside of a Flare function (@export)?"
        )


class MathOp(FlareValue):
    def __init__(self, name: str, *args):
        self.name = name
        self.args = args

    def _best_leaf(self):
        for arg in self.args:
            if hasattr(arg, "_best_leaf"):
                return arg._best_leaf()
        return self.args[0]

    def _alloc_temp(self, prefix="!temp", like=None):
        if like is not None:
            return like._alloc_temp(prefix=prefix)
        leaf = self._best_leaf()
        if hasattr(leaf, "_alloc_temp"):
            return leaf._alloc_temp(prefix=prefix)
        raise TypeError(f"Cannot determine temp allocation for MathOp {self.name}")

    def _compile_into(self, dest):
        from ..math import _dispatch_eval

        return _dispatch_eval(self.name, dest, *self.args)


class LazyOp(FlareValue):
    @property
    def _type(self):
        leaf = self._best_leaf()
        return getattr(leaf, "_type", None)

    def is_sequence(self):
        leaf = self._best_leaf()
        return getattr(leaf, "is_sequence", lambda: False)()

    def __init__(
            self,
            operand,
            eval_fn,
            alloc_temp_fn=None,
            make_copy_fn=None,
            op_name=None,
            op_args=None,
    ):
        self.operand = operand
        self.eval_fn = eval_fn
        self.alloc_temp_fn = alloc_temp_fn
        self._make_copy_fn = make_copy_fn
        self.op_name = op_name
        self.op_args = op_args

    def __icopy__(self, varid: str):
        from .. import context as ctx

        if self._make_copy_fn is not None:
            t = self._make_copy_fn(varid)
        else:
            t = self._alloc_temp()
            t._addr = f"{ctx._current_namespace}:vars {varid}"
        self._compile_into(t)
        return t

    def __getitem__(self, item):
        temp = self._alloc_temp()
        self._compile_into(temp)
        return temp[item]

    def _best_leaf(self):
        if self.alloc_temp_fn is not None:
            return self._alloc_temp()
        return self.operand._best_leaf()

    def _alloc_temp(self, prefix="!temp", like=None):
        if self.alloc_temp_fn is not None:
            return self.alloc_temp_fn()
        if like is not None:
            return like._alloc_temp(prefix=prefix)
        return self.operand._alloc_temp(prefix=prefix)

    def _compile_into(self, dest):
        return self.eval_fn(dest)

    def __branch__(self, invert=False):
        return BinaryOp(self, 0, "ne").__branch__(invert)


class UnsupportedOperandError(Exception):
    def __init__(self, a, op, b):
        super().__init__(
            f"Unsupported operand type(s) for {op}: '{type(a).__name__}' and '{type(b).__name__}'"
        )


def addr(var):
    return var._addr


class macro:
    _is_macro_param = True

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        from .. import context as ctx
        ctx._macro_substituted_raw = True
        return f"$({self.name})"

    def __format__(self, format_spec):
        return format(str(self), format_spec)

    def __repr__(self):
        return f"macro({self.name!r})"

    def _bad_op(self, *_):
        raise TypeError(
            f"Macro '{self.name}' cannot be used in arithmetic expressions. "
            "Use it inside commands or NBT string assignments."
        )

    __add__ = __radd__ = __sub__ = __rsub__ = __mul__ = __rmul__ = _bad_op


def is_lazy(obj):
    return (
            hasattr(type(obj), "_compile_into")
            and getattr(type(obj), "_compile_into") is not FlareValue._compile_into
    )


class ref:
    def __init__(self, target):
        self._target = target

    def __icopy__(self, varid: str):
        return self._target


from .string import NBTStringMethods

LazyOp.__bases__ = (FlareValue, NBTStringMethods)
