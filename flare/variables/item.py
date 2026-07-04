from typing import Optional

from flare.generated.data_component import *


class item:
    def __init__(
            self,
            id: str,
            attack_range: Optional[Union["AttackRange", Any]] = None,
            attribute_modifiers: Optional[Union["AttributeModifiers", Any]] = None,
            banner_patterns: Optional[Union["BannerPatterns", Any]] = None,
            base_color: Optional[Union[Union[str, int], Any]] = None,
            bees: Optional[Union["Bees", Any]] = None,
            block_entity_data: Optional[Union["BlockEntityData", Any]] = None,
            block_state: Optional[Union["BlockState", Any]] = None,
            block_transformer: Optional[Union["BlockTransformer", Any]] = None,
            blocks_attacks: Optional[Union[blocks_attacks, Any]] = None,
            break_sound: Optional[Union["BreakSound", Any]] = None,
            bucket_entity_data: Optional[Union["BucketEntityData", Any]] = None,
            bundle_contents: Optional[Union["BundleContents", Any]] = None,
            can_break: Optional[Union[AdventureModePredicate, Any]] = None,
            can_place_on: Optional[Union[AdventureModePredicate, Any]] = None,
            charged_projectiles: Optional[Union["ChargedProjectiles", Any]] = None,
            consumable: Optional[Union["Consumable", Any]] = None,
            container: Optional[Union["Container", Any]] = None,
            container_loot: Optional[Union["ContainerLoot", Any]] = None,
            custom_data: Optional[Union["CustomData", Any]] = None,
            custom_model_data: Optional[Union[int, Any]] = None,
            custom_name: Optional[Union[Text, Any]] = None,
            damage: Optional[Union[int, Any]] = None,
            damage_resistant: Optional[Union["DamageResistant", Any]] = None,
            damage_type: Optional[Union["DamageType", Any]] = None,
            death_protection: Optional[Union["DeathProtection", Any]] = None,
            debug_stick_state: Optional[Union["DebugStickState", Any]] = None,
            dye: Optional[Union[Union[str, int], Any]] = None,
            dyed_color: Optional[Union[Union[int, dict], Any]] = None,
            enchantable: Optional[Union["Enchantable", Any]] = None,
            enchantment_glint_override: Optional[Union[bool, Any]] = None,
            enchantments: Optional[Union["Enchantments", Any]] = None,
            entity_data: Optional[Union["EntityData", Any]] = None,
            equippable: Optional[Union["Equippable", Any]] = None,
            firework_explosion: Optional[Union["FireworkExplosion", Any]] = None,
            fireworks: Optional[Union["Fireworks", Any]] = None,
            food: Optional[Union["Food", Any]] = None,
            glider: Optional[Union[bool, Any]] = None,
            instrument: Optional[Union[str, Any]] = None,
            intangible_projectile: Optional[Union[bool, Any]] = None,
            item_model: Optional[Union[str, Any]] = None,
            item_name: Optional[Union[Text, Any]] = None,
            jukebox_playable: Optional[Union[Union[str, dict], Any]] = None,
            kinetic_weapon: Optional[Union["KineticWeapon", Any]] = None,
            lock: Optional[Union["Lock", Any]] = None,
            lodestone_tracker: Optional[Union["LodestoneTracker", Any]] = None,
            lore: Optional[Union[Union[list["Text"], "Text"], Any]] = None,
            map_color: Optional[Union[int, Any]] = None,
            map_decorations: Optional[Union["MapDecorations", Any]] = None,
            map_id: Optional[Union[int, Any]] = None,
            max_damage: Optional[Union[int, Any]] = None,
            max_stack_size: Optional[Union[int, Any]] = None,
            minimum_attack_charge: Optional[Union["MinimumAttackCharge", Any]] = None,
            note_block_sound: Optional[Union["NoteBlockSound", Any]] = None,
            ominous_bottle_amplifier: Optional[Union[int, Any]] = None,
            piercing_weapon: Optional[Union["PiercingWeapon", Any]] = None,
            pot_decorations: Optional[Union["PotDecorations", Any]] = None,
            potion_contents: Optional[Union["PotionContents", Any]] = None,
            potion_duration_scale: Optional[Union[float, Any]] = None,
            profile: Optional[Union["Profile", Any]] = None,
            provides_banner_patterns: Optional[Union["ProvidesBannerPatterns", Any]] = None,
            provides_trim_material: Optional[Union["ProvidesTrimMaterial", Any]] = None,
            rarity: Optional[Union["Rarity", Any]] = None,
            recipes: Optional[Union["Recipes", Any]] = None,
            repair_cost: Optional[Union[int, Any]] = None,
            repairable: Optional[Union["Repairable", Any]] = None,
            stored_enchantments: Optional[Union["StoredEnchantments", Any]] = None,
            sulfur_cube_content: Optional[Union["SulfurCubeContent", Any]] = None,
            suspicious_stew_effects: Optional[Union["SuspiciousStewEffects", Any]] = None,
            swing_animation: Optional[Union[bool, Any]] = None,
            tool: Optional[Union["Tool", Any]] = None,
            tooltip_display: Optional[Union["TooltipDisplay", Any]] = None,
            tooltip_style: Optional[Union["TooltipStyle", Any]] = None,
            trim: Optional[Union["Trim", Any]] = None,
            unbreakable: Optional[Union[bool, Any]] = None,
            use_cooldown: Optional[Union[float, Any]] = None,
            use_effects: Optional[Union["UseEffects", Any]] = None,
            use_remainder: Optional[Union[str, Any]] = None,
            weapon: Optional[Union["Weapon", Any]] = None,
            writable_book_content: Optional[Union["WritableBookContent", Any]] = None,
            written_book_content: Optional[Union["WrittenBookContent", Any]] = None,
    ):
        self.id = id
        self.components = {}
        if attack_range is not None:
            self.components["attack_range"] = attack_range
        if attribute_modifiers is not None:
            self.components["attribute_modifiers"] = attribute_modifiers
        if banner_patterns is not None:
            self.components["banner_patterns"] = banner_patterns
        if base_color is not None:
            self.components["base_color"] = base_color
        if bees is not None:
            self.components["bees"] = bees
        if block_entity_data is not None:
            self.components["block_entity_data"] = block_entity_data
        if block_state is not None:
            self.components["block_state"] = block_state
        if block_transformer is not None:
            self.components["block_transformer"] = block_transformer
        if blocks_attacks is not None:
            self.components["blocks_attacks"] = blocks_attacks
        if break_sound is not None:
            self.components["break_sound"] = break_sound
        if bucket_entity_data is not None:
            self.components["bucket_entity_data"] = bucket_entity_data
        if bundle_contents is not None:
            self.components["bundle_contents"] = bundle_contents
        if can_break is not None:
            self.components["can_break"] = can_break
        if can_place_on is not None:
            self.components["can_place_on"] = can_place_on
        if charged_projectiles is not None:
            self.components["charged_projectiles"] = charged_projectiles
        if consumable is not None:
            self.components["consumable"] = consumable
        if container is not None:
            self.components["container"] = container
        if container_loot is not None:
            self.components["container_loot"] = container_loot
        if custom_data is not None:
            self.components["custom_data"] = custom_data
        if custom_model_data is not None:
            self.components["custom_model_data"] = custom_model_data
        if custom_name is not None:
            self.components["custom_name"] = custom_name
        if damage is not None:
            self.components["damage"] = damage
        if damage_resistant is not None:
            self.components["damage_resistant"] = damage_resistant
        if damage_type is not None:
            self.components["damage_type"] = damage_type
        if death_protection is not None:
            self.components["death_protection"] = death_protection
        if debug_stick_state is not None:
            self.components["debug_stick_state"] = debug_stick_state
        if dye is not None:
            self.components["dye"] = dye
        if dyed_color is not None:
            self.components["dyed_color"] = dyed_color
        if enchantable is not None:
            self.components["enchantable"] = enchantable
        if enchantment_glint_override is not None:
            self.components["enchantment_glint_override"] = enchantment_glint_override
        if enchantments is not None:
            self.components["enchantments"] = enchantments
        if entity_data is not None:
            self.components["entity_data"] = entity_data
        if equippable is not None:
            self.components["equippable"] = equippable
        if firework_explosion is not None:
            self.components["firework_explosion"] = firework_explosion
        if fireworks is not None:
            self.components["fireworks"] = fireworks
        if food is not None:
            self.components["food"] = food
        if glider is not None:
            self.components["glider"] = glider
        if instrument is not None:
            self.components["instrument"] = instrument
        if intangible_projectile is not None:
            self.components["intangible_projectile"] = intangible_projectile
        if item_model is not None:
            self.components["item_model"] = item_model
        if item_name is not None:
            self.components["item_name"] = item_name
        if jukebox_playable is not None:
            self.components["jukebox_playable"] = jukebox_playable
        if kinetic_weapon is not None:
            self.components["kinetic_weapon"] = kinetic_weapon
        if lock is not None:
            self.components["lock"] = lock
        if lodestone_tracker is not None:
            self.components["lodestone_tracker"] = lodestone_tracker
        if lore is not None:
            self.components["lore"] = lore
        if map_color is not None:
            self.components["map_color"] = map_color
        if map_decorations is not None:
            self.components["map_decorations"] = map_decorations
        if map_id is not None:
            self.components["map_id"] = map_id
        if max_damage is not None:
            self.components["max_damage"] = max_damage
        if max_stack_size is not None:
            self.components["max_stack_size"] = max_stack_size
        if minimum_attack_charge is not None:
            self.components["minimum_attack_charge"] = minimum_attack_charge
        if note_block_sound is not None:
            self.components["note_block_sound"] = note_block_sound
        if ominous_bottle_amplifier is not None:
            self.components["ominous_bottle_amplifier"] = ominous_bottle_amplifier
        if piercing_weapon is not None:
            self.components["piercing_weapon"] = piercing_weapon
        if pot_decorations is not None:
            self.components["pot_decorations"] = pot_decorations
        if potion_contents is not None:
            self.components["potion_contents"] = potion_contents
        if potion_duration_scale is not None:
            self.components["potion_duration_scale"] = potion_duration_scale
        if profile is not None:
            self.components["profile"] = profile
        if provides_banner_patterns is not None:
            self.components["provides_banner_patterns"] = provides_banner_patterns
        if provides_trim_material is not None:
            self.components["provides_trim_material"] = provides_trim_material
        if rarity is not None:
            self.components["rarity"] = rarity
        if recipes is not None:
            self.components["recipes"] = recipes
        if repair_cost is not None:
            self.components["repair_cost"] = repair_cost
        if repairable is not None:
            self.components["repairable"] = repairable
        if stored_enchantments is not None:
            self.components["stored_enchantments"] = stored_enchantments
        if sulfur_cube_content is not None:
            self.components["sulfur_cube_content"] = sulfur_cube_content
        if suspicious_stew_effects is not None:
            self.components["suspicious_stew_effects"] = suspicious_stew_effects
        if swing_animation is not None:
            self.components["swing_animation"] = swing_animation
        if tool is not None:
            self.components["tool"] = tool
        if tooltip_display is not None:
            self.components["tooltip_display"] = tooltip_display
        if tooltip_style is not None:
            self.components["tooltip_style"] = tooltip_style
        if trim is not None:
            self.components["trim"] = trim
        if unbreakable is not None:
            self.components["unbreakable"] = unbreakable
        if use_cooldown is not None:
            self.components["use_cooldown"] = use_cooldown
        if use_effects is not None:
            self.components["use_effects"] = use_effects
        if use_remainder is not None:
            self.components["use_remainder"] = use_remainder
        if weapon is not None:
            self.components["weapon"] = weapon
        if writable_book_content is not None:
            self.components["writable_book_content"] = writable_book_content
        if written_book_content is not None:
            self.components["written_book_content"] = written_book_content

    def __str__(self):
        import json
        if not self.components:
            return self.id

        comp_strs = []
        for key, value in self.components.items():
            if isinstance(value, bool):
                if value:
                    comp_strs.append(key)
                else:
                    comp_strs.append(f"!{key}")
            else:
                if hasattr(value, "__print__"):
                    value = value.__print__()

                if isinstance(value, str):
                    if not (value.startswith("{") or value.startswith("[")):
                        val_str = json.dumps(value)
                    else:
                        val_str = value
                else:
                    val_str = json.dumps(value, separators=(",", ":"))

                comp_strs.append(f"{key}={val_str}")

        return f"{self.id}[{",".join(comp_strs)}]"
