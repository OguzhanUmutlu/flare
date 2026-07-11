from flare import *

self = selector("@s")
temp_self = selector("@p[tag=we_temp_player]")
players = selector("@a")
here = block("~ ~ ~")

namespace("_rld")


class Vec3:
    def __init__(self, x, y, z):
        self.x = ref(x)
        self.y = ref(y)
        self.z = ref(z)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __getitem__(self, idx):
        return [self.x, self.y, self.z][idx]


pos1, pos2, vec_out = [
    Vec3(self.score(f"we_{i}_x"), self.score(f"we_{i}_y"), self.score(f"we_{i}_z")) for i in ("pos1", "pos2", "out")
]


@export
def raycast() -> int:
    if here == "#minecraft:replaceable":
        with positioned("^ ^ ^0.5"):
            return raycast()
    self.add_tag("we_temp_player")
    with summon("marker"):
        for i, v in enumerate("xyz"):
            temp_self.score(f"we_out_{v}")[:] = self.Pos[i]
        self.kill()
    self.remove_tag("we_temp_player")
    return 0


@export
def kill_edges(u0: macro, u1: macro, u2: macro, u3: macro):
    selector(f"@e[tag=we_bound{u0}_{u1}_{u2}_{u3}]").kill()


@export
def summon_edge(ex: macro, ey: macro, ez: macro, sx: macro, sy: macro, sz: macro, u0: macro, u1: macro, u2: macro,
                u3: macro):
    runcommand(
        f"$summon block_display {ex} {ey} {ez} {{Tags:[\"we_bound{u0}_{u1}_{u2}_{u3}\"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[{sx}f,{sy}f,{sz}f],translation:[0f,0f,0f]}},block_state:{{Name:red_mushroom_block}}}}"
    )


@export
def render_player_bound():
    kill_edges(self.UUID[0], self.UUID[1], self.UUID[2], self.UUID[3])

    if not pos1.x: return
    if not pos2.x: return

    min_x, max_x = min(pos1.x, pos2.x), max(pos1.x, pos2.x)
    min_y, max_y = min(pos1.y, pos2.y), max(pos1.y, pos2.y)
    min_z, max_z = min(pos1.z, pos2.z), max(pos1.z, pos2.z)

    dx = max_x - min_x + 1
    dy = max_y - min_y + 1
    dz = max_z - min_z + 1

    t = 0.05

    x_min, x_max = fixed[3](min_x) - t, fixed[3](min_x) + dx
    y_min, y_max = fixed[3](min_y) - t, fixed[3](min_y) + dy
    z_min, z_max = fixed[3](min_z) - t, fixed[3](min_z) + dz

    len_x = fixed[3](dx) + 2 * t
    len_y = fixed[3](dy) + 2 * t
    len_z = fixed[3](dz) + 2 * t

    for y in (y_min, y_max):
        for z in (z_min, z_max):
            summon_edge(x_min + 0.001, y, z + 0.001, len_x, t, t, self.UUID[0], self.UUID[1], self.UUID[2],
                        self.UUID[3])

    for x in (x_min, x_max):
        for z in (z_min, z_max):
            summon_edge(x + 0.001, y_min, z + 0.001, t, len_y, t, self.UUID[0], self.UUID[1], self.UUID[2],
                        self.UUID[3])

    for x in (x_min, x_max):
        for y in (y_min, y_max):
            summon_edge(x + 0.001, y, z_min + 0.001, t, t, len_z, self.UUID[0], self.UUID[1], self.UUID[2],
                        self.UUID[3])


def raycast_eyes():
    with anchored("eyes"):
        raycast()


@export
def on_wand_punch():
    raycast_eyes()
    for i in range(3):
        pos1[i][:] = vec_out[i]
    self.actionbar("Pos1 set to: X:", pos1.x, "Y:", pos1.y, "Z:", pos1.z, color="gray")
    render_player_bound()


@right_click_event({"minecraft:custom_data": {"flare_worldedit": True}}, once=True, name="on_wand_use")
def on_wand_use():
    raycast_eyes()
    for i in range(3):
        pos2[i][:] = vec_out[i]
    self.actionbar("Pos2 set to: X:", pos2.x, "Y:", pos2.y, "Z:", pos2.z, color="gray")
    render_player_bound()


ench = left_click_enchantment(on_wand_punch)


@export
def internal_fill(x1: macro, x2: macro, y1: macro, y2: macro, z1: macro, z2: macro, block: macro):
    runcommand(f"fill {x1} {y1} {z1} {x2} {y2} {z2} {block}")


def selection_size():
    return (abs(pos2.x - pos1.x) + 1) * (abs(pos2.y - pos1.y) + 1) * (abs(pos2.z - pos1.z) + 1)


@export("we:wand")
def wand():
    self.give_item(
        item(
            "music_disc_5",
            jukebox_playable=False,
            item_name=style("Wand", color="gold"),
            item_model="wooden_axe",
            lore=[
                style("Left click for pos1", color="light_purple", italic=False),
                style("Right click for pos2", color="light_purple", italic=False),
            ],
            piercing_weapon={"min_reach": 0.0, "max_reach": 0.0, "hitbox_margin": 0.0},
            enchantments={ench: 1},
            tooltip_display={"hidden_components": ["minecraft:enchantments"]},
            enchantment_glint_override=False,
            max_stack_size=1,
            custom_data="{flare_worldedit:1b}",
            consumable={"consume_seconds": 2147483647, "has_consume_particles": False},
            use_effects={"speed_multiplier": 1, "can_sprint": True},
        )
    )


@export("we:size")
def size():
    if not pos1.x or not pos2.x:
        print("No selection made.", color="red")
        return
    print("Size of the selection is:", selection_size(), "blocks", color="yellow")


@export("we:set")
def set(block: macro):
    if not pos1.x or not pos2.x:
        print("No selection made.", color="red")
        return
    internal_fill(pos1.x, pos2.x, pos1.y, pos2.y, pos1.z, pos2.z, block)
    print("Selection filled with ", block, " (", selection_size(), " blocks)", color="green", sep="")


@export("we:cut")
def cut():
    if not pos1.x or not pos2.x:
        print("No selection made.", color="red")
        return
    internal_fill(pos1.x, pos2.x, pos1.y, pos2.y, pos1.z, pos2.z, "air")
    print("Selection cut. (", selection_size(), " blocks)", color="green", sep="")


namespace("rld_test")

for player in players:
    player.clear_inventory()
    wand()
    render_player_bound()
