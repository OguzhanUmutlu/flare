### AUTO GENERATED DO NOT EDIT ###
from flare.variables.nbt import struct
from flare.types import byte, short, long, double
from flare.basesymbols import *
from typing import Any

@struct
class TestData:
    environment: Any
    structure: str
    max_ticks: int
    setup_ticks: int
    required: bool
    rotation: 'Any'
    manual_only: bool
    max_attempts: int
    required_successes: int
    sky_access: bool
    padding: int

@struct
class FunctionTestInstance(TestData):
    function: str

@struct
class BlockBasedTestInstance(TestData):
    pass