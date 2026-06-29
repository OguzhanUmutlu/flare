### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any, Union

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
class FunctionTestInstance(TestData):
    function: str

@struct
class TestEnvironment:
    type: str

@struct
class BlockBasedTestInstance(TestData):
    pass