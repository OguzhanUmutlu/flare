import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import flare
import mcemu.commands
from mcemu.command_tree.dispatcher import dispatcher

from flare import score, nbt, namespace, export
from flare.variables import getscore
from flare.types import NBTType
from flare.control_flow import _flare_if, _flare_for, _flare_while
from flare.context import runcommand, files
import mcemu
import mcemu.commands


def test_import():
    assert flare is not None


def test_function_commands():
    emu = mcemu.Emulator()
    emu.execute_command("scoreboard objectives add dummy dummy")
    print("Initial var1:", emu.world.get_score("var1", "dummy"))
    res = emu.execute_file("test.mcfunction")
    print("Return value:", res)
    print("After var1:", emu.world.get_score("var1", "dummy"))

    emu.execute_command("schedule function test.mcfunction 5s")
    print("Scheduled tasks:", emu.world.scheduled_tasks)
    emu.execute_command("tick step 99")
    print("Scheduled tasks after step:", emu.world.scheduled_tasks)


def test_if():
    a = score(addr="a obj")
    b = score(addr="b obj")
    c = score(addr="c obj")
    d = score(addr="d obj")
    e = score(addr="e obj")

    def body_1():
        runcommand("say hi")

    def body_2():
        runcommand("say not hi")

    def cond1():
        return ((a == b) | (a == c)) & ((a == d) | (c == e))

    _flare_if(cond1, None, body_1, body_2)

    print("\n--- Generated Files ---")
    for filename, commands in files.items():
        print(f"\n[{filename}]")
        for cmd in commands:
            print("  " + cmd)


def test_loops():
    namespace("test")

    my_list = nbt(addr="storage test:data list", datatype=NBTType.List)
    x = getscore(5)
    y = getscore(0)

    @export
    def process_list():
        def loop_body(item):
            runcommand(f"say Got item from list")

        _flare_for(my_list, loop_body)

    @export(append=True)
    def process_list():
        def while_cond():
            return y < x

        def while_body():
            y.__iadd__(1)
            runcommand("say looping!")

        _flare_while(while_cond, while_body)

    print("\n--- Generated Files ---")
    for filename, commands in files.items():
        print(f"\n[{filename}]")
        for cmd in commands:
            print("  " + cmd)


def test_parse():
    print("dispatcher id:", id(dispatcher))
    print("children keys:", dispatcher.root.children.keys())
