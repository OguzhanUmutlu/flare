from flare import *

namespace("worldedit")

self = selector("@s")
players = selector("@a")

add_enchantment("wand_punch", {
    "description": "",
    "supported_items": [],
    "weight": 1,
    "max_level": 1,
    "min_cost": {
        "base": 0,
        "per_level_above_first": 0
    },
    "max_cost": {
        "base": 0,
        "per_level_above_first": 0
    },
    "anvil_cost": 0,
    "slots": ["hand"],
    "effects": {
        "minecraft:post_piercing_attack": [
            {
                "effect": {
                    "type": "minecraft:run_function",
                    "function": "worldedit:on_wand_punch"
                }
            }
        ]
    }
})


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
                style("Right click for pos1", color="light_purple", italic=False)
            ],
            piercing_weapon={"min_reach": 0.0, "max_reach": 0.0, "hitbox_margin": 0.0},
            enchantments={"worldedit:wand_punch": 1},
            tooltip_display={"hidden_components": ["minecraft:enchantments"]},
            enchantment_glint_override=False,
            max_stack_size=1,
            custom_data="{flare_worldedit:1b}"
        )
    )


@export
def on_wand_punch():
    print("hi")


@tick
def tick():
    for player in players:
        if player.has_item("weapon.mainhand", "wooden_axe[custom_data={flare_worldedit:true}]"):
            print("hi")
