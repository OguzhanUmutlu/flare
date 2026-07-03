### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
import typing
from typing import Any
if typing.TYPE_CHECKING:
    from typing import Union
else:

    class _DummyUnion:

        def __getitem__(self, items):
            return typing.Any
    Union = _DummyUnion()

@struct
class TestData:
    environment: Union[str, 'TestEnvironment']
    structure: str
    max_ticks: int
    setup_ticks: int
    required: bool
    rotation: 'Rotation'
    manual_only: bool
    max_attempts: int
    required_successes: int
    sky_access: bool
    padding: int

@struct
class BlockBasedTestInstance(TestData):
    pass

@struct
class FunctionTestInstance(TestData):
    function: str

@struct
class TestEnvironment:
    type: str