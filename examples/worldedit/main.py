from flare import *
from flare.context import ensure_objective

self = selector("@s")
players = selector("@a")
here = block("~ ~ ~")

add_enchantment("wand_punch", Enchantment(
    description="",
    supported_items=[],
    weight=1,
    max_level=1,
    min_cost={"base": 0, "per_level_above_first": 0},
    max_cost={"base": 0, "per_level_above_first": 0},
    anvil_cost=0,
    slots=["hand"],
    effects={
        "minecraft:post_piercing_attack": [
            {
                "effect": {
                    "type": "minecraft:run_function",
                    "function": "we:on_wand_punch"
                }
            }
        ]
    }
))


@export
def wand():
    self.give_item(
        item(
            "music_disc_5",
            jukebox_playable=False,
            item_name=style("Wand", color="gold"),
            item_model="wooden_axe",
            lore=[
                style("Left click for pos1", color="light_purple", italic=False),
                style("Right click for pos2", color="light_purple", italic=False)
            ],
            piercing_weapon={"min_reach": 0.0, "max_reach": 0.0, "hitbox_margin": 0.0},
            enchantments={"we:wand_punch": 1},
            tooltip_display={"hidden_components": ["minecraft:enchantments"]},
            enchantment_glint_override=False,
            max_stack_size=1,
            custom_data="{flare_worldedit:1b}",
            consumable={"consume_seconds": 2147483647, "has_consume_particles": False},
            use_effects={"speed_multiplier": 1, "can_sprint": True}
        )
    )


@export
def raycast() -> int:
    if here == "#minecraft:replaceable":
        with positioned("^ ^ ^0.5"):
            return raycast()
    here.setblock("stone")
    return 0


@export
def on_wand_punch():
    raycast()


wand_use_cooldown = Objective("wand_cooldown")
ensure_objective(wand_use_cooldown.name)


@tick_event()
@using_item_event({"item": {"predicates": {"minecraft:custom_data": {"flare_worldedit": True}}}})
def on_wand_use():
    cd = ref(wand_use_cooldown[self])
    if not (cd >= 1):
        with anchored("eyes"):
            block("^ ^ ^3").add_particles("happy_villager", "0.1 0.1 0.1", 0, 10)
            print("right click")

    cd = 2


@tick
def tick():
    for player in players:
        if player.has_item("weapon.mainhand", "wooden_axe[custom_data={flare_worldedit:true}]"):
            print("hi")


with players:
    self.clear_inventory()
    wand()
