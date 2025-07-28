from __future__ import annotations

from flare.modules.bolt_help import function, run

objectives: set[str] = set()


class Score:
    def __init__(self, objective: str, target: str):
        self.objective = objective
        self.target = target
        if objective not in objectives:
            with function("flare:__init__"):
                run(f"scoreboard objectives add {objective} dummy")
                objectives.add(objective)

    def add(self, other):
        if isinstance(other, float):
            raise ValueError("Cannot add float literal to score directly.")
        if isinstance(other, int):
            if other < 0:
                self.sub(-other)
                return
            run(f"scoreboard players add {self} {other}")
        elif isinstance(other, Score):
            run(f"scoreboard players operation {self} += {other}")
        elif isinstance(other, NBT):
            if not other.is_integer:
                raise ValueError("Cannot add non-integer NBT to score directly.")
            other_score = score()
            other_score.set(other)
            self.add(other_score)
        else:
            raise TypeError(f"Unsupported type for addition: {type(other)}")

    def sub(self, other):
        if isinstance(other, float):
            raise ValueError("Cannot subtract float literal to score directly.")
        if isinstance(other, int):
            if other < 0:
                self.add(-other)
                return
            run(f"scoreboard players remove {self} {other}")
        elif isinstance(other, Score):
            run(f"scoreboard players operation {self} -= {other}")
        elif isinstance(other, NBT):
            run(f"execute store result score {self} run data get {other.target} {other.path}")
        else:
            raise TypeError(f"Unsupported type for addition: {type(other)}")

    def mul(self, other):
        if isinstance(other, float):
            raise ValueError("Cannot multiply score by float literal directly.")
        if isinstance(other, int):
            if other == 1:
                return
            if other == 0:
                run(f"scoreboard players set {self} 0")
                return
            self.mul(int_score(other))
        elif isinstance(other, Score):
            run(f"scoreboard players operation {self} *= {other}")
        elif isinstance(other, NBT):
            if not other.is_integer:
                raise ValueError("Cannot multiply score by non-integer NBT directly.")
            other_score = score()
            other_score.set(other)
            self.mul(other_score)
        else:
            raise TypeError(f"Unsupported type for multiplication: {type(other)}")

    def div(self, other):
        if isinstance(other, float):
            raise ValueError("Cannot divide score by float literal directly.")
        if isinstance(other, int):
            if other == 1:
                return
            if other == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
            self.div(int_score(other))
        elif isinstance(other, Score):
            run(f"scoreboard players operation {self} /= {other}")
        elif isinstance(other, NBT):
            if not other.is_integer:
                raise ValueError("Cannot divide score by non-integer NBT directly.")
            other_score = score()
            other_score.set(other)
            self.div(other_score)
        else:
            raise TypeError(f"Unsupported type for division: {type(other)}")

    def mod(self, other):
        if isinstance(other, float):
            raise ValueError("Cannot mod score by float literal directly.")
        if isinstance(other, int):
            if other == 1:
                return
            if other == 0:
                raise ZeroDivisionError("Cannot mod by zero.")
            self.mod(int_score(other))
        elif isinstance(other, Score):
            run(f"scoreboard players operation {self} %= {other}")
        elif isinstance(other, NBT):
            if not other.is_integer:
                raise ValueError("Cannot mod score by non-integer NBT directly.")
            self.mod(score(other))
        else:
            raise TypeError(f"Unsupported type for modulo: {type(other)}")

    def set(self, other):
        if isinstance(other, float):
            raise ValueError("Cannot copy float literal to score directly.")
        if isinstance(other, int):
            run(f"scoreboard players set {self} {other}")
        elif isinstance(other, Score):
            run(f"scoreboard players operation {self} = {other}")
        elif isinstance(other, NBT):
            if not other.is_integer:
                raise ValueError("Cannot copy non-integer NBT to score directly.")
            sc = score()
            run(f"execute store result score {sc.target} {sc.objective} run data get {other}")
            self.set(sc)
        else:
            raise TypeError(f"Unsupported type for copy: {type(other)}")

    def __str__(self):
        return f"{self.objective} {self.target}"

    def __repr__(self):
        return f"Score(objective={self.objective!r}, target={self.target!r})"


from flare.modules.nbt import NBT
from flare.modules.utils import score, int_score
