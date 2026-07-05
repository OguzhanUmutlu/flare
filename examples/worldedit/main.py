from flare import *

self = selector("@s")
players = selector("@a")
here = block("~ ~ ~")


@export
def raycast() -> int:
    if here == "#minecraft:replaceable":
        with positioned("^ ^ ^0.5"):
            return raycast()
    here.setblock("stone")
    return 0


def raycast_eyes():
    anchored("eyes").then(lambda: raycast())


@export
def on_wand_punch():
    raycast_eyes()


@right_click_event({"minecraft:custom_data": {"flare_worldedit": True}}, once=True)
def on_wand_use():
    raycast_eyes()


ench = left_click_enchantment(on_wand_punch)


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
            enchantments={ench: 1},
            tooltip_display={"hidden_components": ["minecraft:enchantments"]},
            enchantment_glint_override=False,
            max_stack_size=1,
            custom_data="{flare_worldedit:1b}",
            consumable={"consume_seconds": 2147483647, "has_consume_particles": False},
            use_effects={"speed_multiplier": 1, "can_sprint": True}
        )
    )


@tick
def tick():
    for player in players:
        if player.has_item("weapon.mainhand", "wooden_axe[custom_data={flare_worldedit:true}]"):
            print("hi")


for player in players:
    player.clear_inventory()
    wand()
