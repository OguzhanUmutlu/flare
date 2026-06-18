from .types import NBTType

_B = NBTType.Byte
_S = NBTType.Short
_I = NBTType.Int
_L = NBTType.Long
_F = NBTType.Float
_D = NBTType.Double
_BA = NBTType.ByteArray
_STR = NBTType.String
_LS = NBTType.List
_C = NBTType.Compound
_IA = NBTType.IntArray
_LA = NBTType.LongArray

ENTITY_SCHEMA = {
    'type': _C,
    'children': {
        'DataVersion': {
            'type': _C,
            'children': {
                'DataVersion': {'type': _I, 'children': {}},
                'Position': {
                    'type': _IA,
                    'children': {
                        '[]': {'type': _I, 'children': {}}
                    }
                },
                'Entities': {
                    'type': _LS,
                    'children': {
                        '[]': {'type': _C, 'children': {}}
                    }
                }
            }
        },
        'Air': {
            'type': _S,
            'children': {
                'Air': {'type': _S, 'children': {}},
                'CustomName': {'type': _C, 'children': {}},
                'CustomNameVisible': {'type': _B, 'children': {}},
                'data': {'type': _C, 'children': {}},
                'fall_distance': {'type': _D, 'children': {}},
                'Fire': {'type': _S, 'children': {}},
                'Glowing': {'type': _B, 'children': {}},
                'HasVisualFire': {'type': _B, 'children': {}},
                'id': {'type': _STR, 'children': {}},
                'Invulnerable': {'type': _B, 'children': {}},
                'Motion': {'type': _LS, 'children': {}},
                'NoGravity': {'type': _B, 'children': {}},
                'OnGround': {'type': _B, 'children': {}},
                'Passengers': {'type': _LS, 'children': {'[]': 'RECURSIVE_PASSENGERS'}},
                'PortalCooldown': {'type': _I, 'children': {}},
                'Pos': {'type': _LS, 'children': {}},
                'Rotation': {
                    'type': _LS,
                    'children': {
                        '[]': {'type': _F, 'children': {}}
                    }
                },
                'Silent': {'type': _B, 'children': {}},
                'Tags': {'type': _LS, 'children': {}},
                'TicksFrozen': {'type': _I, 'children': {}},
                'UUID': {'type': _IA, 'children': {}}
            }
        },
        'AbsorptionAmount': {
            'type': _F,
            'children': {
                'AbsorptionAmount': {'type': _F, 'children': {}},
                'active_effects': {
                    'type': _LS,
                    'children': {
                        '[]': {
                            'type': _C,
                            'children': {
                                'ambient': {'type': _B, 'children': {}},
                                'amplifier': {'type': _B, 'children': {}},
                                'duration': {'type': _I, 'children': {}},
                                'hidden_effect': {'type': _C, 'children': {}},
                                'id': {'type': _STR, 'children': {}},
                                'show_icon': {'type': _B, 'children': {}},
                                'show_particles': {'type': _B, 'children': {}}
                            }
                        }
                    }
                },
                'attributes': {
                    'type': _LS,
                    'children': {
                        '[]': {
                            'type': _C,
                            'children': {
                                'id': {'type': _STR, 'children': {}},
                                'base': {'type': _D, 'children': {}},
                                'modifiers': {
                                    'type': _LS,
                                    'children': {
                                        '[]': {
                                            'type': _C,
                                            'children': {
                                                'amount': {},
                                                'id': {},
                                                'operation': {}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                'Brain': {
                    'type': _C,
                    'children': {
                        'memories': {'type': _C, 'children': {}}
                    }
                },
                'CanPickUpLoot': {'type': _B, 'children': {}},
                'current_explosion_impact_pos': {'type': _LS, 'children': {}},
                'current_impulse_context_reset_grace_time': {'type': _I, 'children': {}},
                'DeathTime': {'type': _S, 'children': {}},
                'drop_chances': {
                    'type': _C,
                    'children': {
                        'head': {'type': _F, 'children': {}},
                        'chest': {'type': _F, 'children': {}},
                        'legs': {'type': _F, 'children': {}},
                        'feet': {'type': _F, 'children': {}},
                        'mainhand': {'type': _F, 'children': {}},
                        'offhand': {'type': _F, 'children': {}},
                        'body': {'type': _F, 'children': {}},
                        'saddle': {'type': _F, 'children': {}}
                    }
                },
                'equipment': {
                    'type': _C,
                    'children': {
                        'head': {'type': _C, 'children': {}},
                        'chest': {'type': _C, 'children': {}},
                        'legs': {'type': _C, 'children': {}},
                        'feet': {'type': _C, 'children': {}},
                        'mainhand': {'type': _C, 'children': {}},
                        'offhand': {'type': _C, 'children': {}},
                        'body': {'type': _C, 'children': {}},
                        'saddle': {'type': _C, 'children': {}}
                    }
                },
                'FallFlying': {'type': _B, 'children': {}},
                'Health': {'type': _F, 'children': {}},
                'home_pos': {'type': _IA, 'children': {}},
                'home_radius': {'type': _I, 'children': {}},
                'HurtByTimestamp': {'type': _I, 'children': {}},
                'HurtTime': {'type': _S, 'children': {}},
                'last_hurt_by_mob': {'type': _IA, 'children': {}},
                'last_hurt_by_player': {'type': _IA, 'children': {}},
                'last_hurt_by_player_memory_time': {'type': _I, 'children': {}},
                'leash': {
                    'type': _C,
                    'children': {
                        '[]': {'type': _C, 'children': {}},
                        'UUID': {'type': _IA, 'children': {}}
                    }
                },
                'LeftHanded': {'type': _B, 'children': {}},
                'locator_bar_icon': {
                    'type': _C,
                    'children': {
                        'color': {'type': _I, 'children': {}},
                        'style': {'type': _STR, 'children': {}}
                    }
                },
                'NoAI': {'type': _B, 'children': {}},
                'PersistenceRequired': {'type': _B, 'children': {}},
                'sleeping_pos': {'type': _IA, 'children': {}},
                'Team': {'type': _STR, 'children': {}},
                'ticks_since_last_hurt_by_mob': {'type': _I, 'children': {}}
            }
        },
        'DuplicationCooldown': {
            'type': _C,
            'children': {
                'DuplicationCooldown': {'type': _L, 'children': {}},
                'Inventory': {'type': _LS, 'children': {}},
                'listener': {
                    'type': _C,
                    'children': {
                        'distance': {'type': _I, 'children': {}},
                        'event': {
                            'type': _C,
                            'children': {
                                'distance': {'type': _I, 'children': {}},
                                'game_event': {'type': _STR, 'children': {}},
                                'pos': {'type': _LS, 'children': {}},
                                'projectile_owner': {'type': _IA, 'children': {}},
                                'source': {'type': _IA, 'children': {}}
                            }
                        },
                        'event_delay': {'type': _I, 'children': {}},
                        'event_distance': {'type': _I, 'children': {}},
                        'range': {'type': _I, 'children': {}},
                        'source': {
                            'type': _C,
                            'children': {
                                'type': {'type': _STR, 'children': {}},
                                'pos': {
                                    'type': _IA,
                                    'children': {
                                        'pos': {'type': _IA, 'children': {}}
                                    }
                                },
                                'source_entity': {
                                    'type': _IA,
                                    'children': {
                                        'source_entity': {'type': _IA, 'children': {}},
                                        'y_offset': {'type': _F, 'children': {}}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        'scute_time': {
            'type': _C,
            'children': {
                'scute_time': {'type': _I, 'children': {}},
                'state': {'type': _STR, 'children': {}}
            }
        },
        'DisabledSlots': {
            'type': _C,
            'children': {
                'DisabledSlots': {'type': _I, 'children': {}},
                'Invisible': {'type': _B, 'children': {}},
                'Marker': {'type': _B, 'children': {}},
                'NoBasePlate': {'type': _B, 'children': {}},
                'Pose': {
                    'type': _C,
                    'children': {
                        'Body': {
                            'type': _LS,
                            'children': {
                                '[]': {'type': _F, 'children': {}}
                            }
                        },
                        'Head': {
                            'type': _LS,
                            'children': {
                                '[]': {'type': _F, 'children': {}}
                            }
                        },
                        'LeftArm': {
                            'type': _LS,
                            'children': {
                                '[]': {'type': _F, 'children': {}}
                            }
                        },
                        'LeftLeg': {
                            'type': _LS,
                            'children': {
                                '[]': {'type': _F, 'children': {}}
                            }
                        },
                        'RightArm': {
                            'type': _LS,
                            'children': {
                                '[]': {'type': _F, 'children': {}}
                            }
                        },
                        'RightLeg': {
                            'type': _LS,
                            'children': {
                                '[]': {'type': _F, 'children': {}}
                            }
                        }
                    }
                },
                'ShowArms': {'type': _B, 'children': {}},
                'Small': {'type': _B, 'children': {}}
            }
        },
        'FromBucket': {
            'type': _C,
            'children': {
                'FromBucket': {'type': _B, 'children': {}},
                'Variant': {'type': _I, 'children': {}},
                'PuffState': {'type': _I, 'children': {}},
                'type': {'type': _STR, 'children': {}}
            }
        },
        'BatFlags': {
            'type': _C,
            'children': {
                'BatFlags': {'type': _B, 'children': {}}
            }
        },
        'CannotEnterHiveTicks': {
            'type': _C,
            'children': {
                'CannotEnterHiveTicks': {'type': _I, 'children': {}},
                'CropsGrownSincePollination': {'type': _I, 'children': {}},
                'flower_pos': {'type': _IA, 'children': {}},
                'HasNectar': {'type': _B, 'children': {}},
                'HasStung': {'type': _B, 'children': {}},
                'hive_pos': {'type': _IA, 'children': {}},
                'TicksSincePollination': {'type': _I, 'children': {}}
            }
        },
        'Bred': {
            'type': _C,
            'children': {
                'Bred': {'type': _B, 'children': {}},
                'EatingHaystack': {'type': _B, 'children': {}},
                'Owner': {'type': _IA, 'children': {}},
                'Tame': {'type': _B, 'children': {}},
                'Temper': {'type': _I, 'children': {}},
                'LastPoseTick': {'type': _L, 'children': {}},
                'ChestedHorse': {'type': _B, 'children': {}},
                'Items': {
                    'type': _LS,
                    'children': {
                        '[]': {'type': _C, 'children': {}}
                    }
                },
                'Variant': {'type': _I, 'children': {}},
                'DespawnDelay': {'type': _I, 'children': {}},
                'Strength': {'type': _I, 'children': {}},
                'SkeletonTrap': {'type': _B, 'children': {}},
                'SkeletonTrapTime': {'type': _I, 'children': {}}
            }
        },
        'CollarColor': {
            'type': _C,
            'children': {
                'CollarColor': {'type': _B, 'children': {}},
                'variant': {'type': _STR, 'children': {}},
                'sound_variant': {'type': _STR, 'children': {}}
            }
        },
        'EggLayTime': {
            'type': _C,
            'children': {
                'EggLayTime': {'type': _I, 'children': {}},
                'IsChickenJockey': {'type': _B, 'children': {}},
                'variant': {'type': _STR, 'children': {}}
            }
        },
        'weather_state': {
            'type': _C,
            'children': {
                'weather_state': {'type': _STR, 'children': {}},
                'next_weather_age': {'type': _L, 'children': {}}
            }
        },
        'variant': {
            'type': _C,
            'children': {
                'variant': {'type': _STR, 'children': {}}
            }
        },
        'ExplosionRadius': {
            'type': _C,
            'children': {
                'ExplosionRadius': {'type': _B, 'children': {}},
                'Fuse': {'type': _S, 'children': {}},
                'ignited': {'type': _B, 'children': {}},
                'powered': {'type': _B, 'children': {}}
            }
        },
        'Moistness': {
            'type': _C,
            'children': {
                'Moistness': {'type': _I, 'children': {}},
                'GotFish': {'type': _B, 'children': {}}
            }
        },
        'CanBreakDoors': {
            'type': _C,
            'children': {
                'CanBreakDoors': {'type': _B, 'children': {}},
                'DrownedConversionTime': {'type': _I, 'children': {}},
                'InWaterTime': {'type': _I, 'children': {}},
                'IsBaby': {'type': _B, 'children': {}}
            }
        },
        'DragonDeathTime': {
            'type': _C,
            'children': {
                'DragonDeathTime': {'type': _I, 'children': {}},
                'DragonPhase': {'type': _I, 'children': {}},
                'sitting_damage_recieved': {'type': _F, 'children': {}}
            }
        },
        'carriedBlockState': {
            'type': _C,
            'children': {
                'carriedBlockState': {'type': _C, 'children': {}}
            }
        },
        'Lifetime': {
            'type': _C,
            'children': {
                'Lifetime': {'type': _I, 'children': {}}
            }
        },
        'SpellTicks': {
            'type': _C,
            'children': {
                'SpellTicks': {'type': _I, 'children': {}}
            }
        },
        'Crouching': {
            'type': _C,
            'children': {
                'Crouching': {'type': _B, 'children': {}},
                'Sitting': {'type': _B, 'children': {}},
                'Sleeping': {'type': _B, 'children': {}},
                'Trusted': {
                    'type': _LS,
                    'children': {
                        '[]': {'type': _IA, 'children': {}}
                    }
                },
                'Type': {'type': _STR, 'children': {}}
            }
        },
        'ExplosionPower': {
            'type': _C,
            'children': {
                'ExplosionPower': {'type': _B, 'children': {}},
                'Item': {'type': _C, 'children': {}}
            }
        },
        'DarkTicksRemaining': {
            'type': _C,
            'children': {
                'DarkTicksRemaining': {'type': _I, 'children': {}}
            }
        },
        'HasLeftHorn': {
            'type': _C,
            'children': {
                'HasLeftHorn': {'type': _B, 'children': {}},
                'HasRightHorn': {'type': _B, 'children': {}},
                'IsScreamingGoat': {'type': _B, 'children': {}}
            }
        },
        'still_timeout': {
            'type': _C,
            'children': {
                'still_timeout': {'type': _I, 'children': {}}
            }
        },
        'CannotBeHunted': {
            'type': _C,
            'children': {
                'CannotBeHunted': {'type': _B, 'children': {}},
                'IsImmuneToZombification': {'type': _B, 'children': {}},
                'TimeInOverworld': {'type': _I, 'children': {}}
            }
        },
        'PlayerCreated': {
            'type': _C,
            'children': {
                'PlayerCreated': {'type': _B, 'children': {}}
            }
        },
        'profile': {
            'type': _C,
            'children': {
                'profile': {'type': _STR, 'children': {}},
                'hidden_layers': {'type': _LS, 'children': {}},
                'main_hand': {'type': _STR, 'children': {}},
                'pose': {'type': _STR, 'children': {}},
                'immovable': {'type': _B, 'children': {}},
                'description': {'type': _STR, 'children': {}},
                'hide_description': {'type': _B, 'children': {}}
            }
        },
        'stew_effects': {
            'type': _C,
            'children': {
                'stew_effects': {
                    'type': _LS,
                    'children': {
                        '[]': {
                            'type': _C,
                            'children': {
                                'id': {'type': _STR, 'children': {}},
                                'duration': {'type': _I, 'children': {}}
                            }
                        }
                    }
                },
                'Type': {'type': _STR, 'children': {}}
            }
        },
        'Trusting': {
            'type': _C,
            'children': {
                'Trusting': {'type': _B, 'children': {}}
            }
        },
        'HiddenGene': {
            'type': _C,
            'children': {
                'HiddenGene': {'type': _STR, 'children': {}},
                'MainGene': {'type': _STR, 'children': {}}
            }
        },
        'Variant': {
            'type': _C,
            'children': {
                'Variant': {'type': _I, 'children': {}}
            }
        },
        'size': {
            'type': _C,
            'children': {
                'size': {'type': _I, 'children': {}},
                'anchor_pos': {'type': _IA, 'children': {}}
            }
        },
        'CannotHunt': {
            'type': _C,
            'children': {
                'CannotHunt': {'type': _B, 'children': {}},
                'Inventory': {
                    'type': _LS,
                    'children': {
                        '[]': {'type': _C, 'children': {}}
                    }
                },
                'IsBaby': {'type': _B, 'children': {}},
                'IsImmuneToZombification': {'type': _B, 'children': {}},
                'TimeInOverworld': {'type': _I, 'children': {}}
            }
        },
        'IsImmuneToZombification': {
            'type': _C,
            'children': {
                'IsImmuneToZombification': {'type': _B, 'children': {}},
                'TimeInOverworld': {'type': _I, 'children': {}}
            }
        },
        'Inventory': {
            'type': _LS,
            'children': {
                'Inventory': {
                    'type': _LS,
                    'children': {
                        '[]': {'type': _C, 'children': {}}
                    }
                },
                '[]': {
                    'type': _C,
                    'children': {
                        'id': {'type': _STR, 'children': {}},
                        'Count': {'type': _B, 'children': {}},
                        'Slot': {'type': _B, 'children': {}},
                        'tag': {'type': _C, 'children': {}},
                        'components': {
                            'type': _C,
                            'children': {
                                'id': {
                                    'type': _STR,
                                    'children': {
                                        'id': {'type': _STR, 'children': {}},
                                        'keepPacked': {'type': _B, 'children': {}},
                                        'x': {'type': _I, 'children': {}},
                                        'y': {'type': _I, 'children': {}},
                                        'z': {'type': _I, 'children': {}},
                                        'components': {'type': _C, 'children': {}}
                                    }
                                },
                                'components': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:follow': {'type': _B, 'children': {}}
                                    }
                                },
                                'minecraft:attack_range': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:attack_range': {
                                            'type': _C,
                                            'children': {
                                                'min_reach': {},
                                                'max_reach': {},
                                                'min_creative_reach': {},
                                                'max_creative_reach': {},
                                                'hitbox_margin': {},
                                                'mob_factor': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:attribute_modifiers': {
                                    'type': _LS,
                                    'children': {
                                        '[]': {
                                            'type': _LS,
                                            'children': {
                                                '[]': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:block_entity_data': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:block_entity_data': {'type': _C, 'children': {}}
                                    }
                                },
                                'minecraft:blocks_attacks': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:blocks_attacks': {
                                            'type': _C,
                                            'children': {
                                                'block_delay_seconds': {},
                                                'disable_cooldown_scale': {},
                                                'damage_reductions': {},
                                                'item_damage': {},
                                                'block_sound': {},
                                                'disabled_sound': {},
                                                'bypassed_by': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:break_sound': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:break_sound': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:bucket_entity_data': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:bucket_entity_data': {
                                            'type': _C,
                                            'children': {
                                                'NoAI': {},
                                                'Silent': {},
                                                'NoGravity': {},
                                                'Glowing': {},
                                                'Invulnerable': {},
                                                'AgeLocked': {},
                                                'Health': {},
                                                'Age': {},
                                                'HuntingCooldown': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:can_break': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:can_break': {
                                            'type': _C,
                                            'children': {
                                                'blocks': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:can_place_on': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:can_place_on': {
                                            'type': _C,
                                            'children': {
                                                'blocks': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:consumable': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:consumable': {
                                            'type': _C,
                                            'children': {
                                                'consume_seconds': {},
                                                'animation': {},
                                                'sound': {},
                                                'has_consume_particles': {},
                                                'on_consume_effects': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:custom_model_data': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:custom_model_data': {
                                            'type': _C,
                                            'children': {
                                                'floats': {},
                                                'flags': {},
                                                'strings': {},
                                                'colors': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:custom_name': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:custom_name': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:damage_resistant': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:damage_resistant': {
                                            'type': _C,
                                            'children': {
                                                'types': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:damage_type': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:damage_type': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:death_protection': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:death_protection': {
                                            'type': _C,
                                            'children': {
                                                'death_effects': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:enchantable': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:enchantable': {
                                            'type': _C,
                                            'children': {
                                                'value': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:enchantments': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:enchantments': {
                                            'type': _C,
                                            'children': {
                                                '<enchantment ID>': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:equippable': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:equippable': {
                                            'type': _C,
                                            'children': {
                                                'slot': {},
                                                'equip_sound': {},
                                                'asset_id': {},
                                                'allowed_entities': {},
                                                'dispensable': {},
                                                'swappable': {},
                                                'damage_on_hurt': {},
                                                'equip_on_interact': {},
                                                'camera_overlay': {},
                                                'can_be_sheared': {},
                                                'shearing_sound': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:glider': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:glider': {'type': _C, 'children': {}}
                                    }
                                },
                                'minecraft:instrument': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:instrument': {
                                            'type': _STR,
                                            'children': {
                                                'description': {},
                                                'sound_event': {},
                                                'use_duration': {},
                                                'range': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:item_model': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:item_model': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:item_name': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:item_name': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:jukebox_playable': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:jukebox_playable': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:kinetic_weapon': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:kinetic_weapon': {
                                            'type': _C,
                                            'children': {
                                                'delay_ticks': {},
                                                'damage_conditions': {},
                                                'dismount_conditions': {},
                                                'knockback_conditions': {},
                                                'forward_movement': {},
                                                'damage_multiplier': {},
                                                'sound': {},
                                                'hit_sound': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:max_damage': {
                                    'type': _I,
                                    'children': {
                                        'minecraft:max_damage': {'type': _I, 'children': {}}
                                    }
                                },
                                'minecraft:minimum_attack_charge': {
                                    'type': _F,
                                    'children': {
                                        'minecraft:minimum_attack_charge': {'type': _F, 'children': {}}
                                    }
                                },
                                'minecraft:piercing_weapon': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:piercing_weapon': {
                                            'type': _C,
                                            'children': {
                                                'deals_knockback': {},
                                                'dismounts': {},
                                                'sound': {},
                                                'hit_sound': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:potion_contents': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:potion_contents': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:potion_duration_scale': {
                                    'type': _F,
                                    'children': {
                                        'minecraft:potion_duration_scale': {'type': _F, 'children': {}}
                                    }
                                },
                                'minecraft:profile': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:profile': {'type': _STR, 'children': {}},
                                        'name': {
                                            'type': _STR,
                                            'children': {
                                                'name': {},
                                                'id': {},
                                                'properties': {},
                                                'texture': {},
                                                'cape': {},
                                                'elytra': {},
                                                'model': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:provides_banner_patterns': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:provides_banner_patterns': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:provides_trim_material': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:provides_trim_material': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:repairable': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:repairable': {
                                            'type': _C,
                                            'children': {
                                                'items': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:stored_enchantments': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:stored_enchantments': {
                                            'type': _C,
                                            'children': {
                                                '<enchantment ID>': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:swing_animation': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:swing_animation': {
                                            'type': _C,
                                            'children': {
                                                'type': {},
                                                'duration': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:tooltip_display': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:tooltip_display': {
                                            'type': _C,
                                            'children': {
                                                'hide_tooltip': {},
                                                'hidden_components': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:tooltip_style': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:tooltip_style': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:use_cooldown': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:use_cooldown': {
                                            'type': _C,
                                            'children': {
                                                'seconds': {},
                                                'cooldown_group': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:use_effects': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:use_effects': {
                                            'type': _C,
                                            'children': {
                                                'can_sprint': {},
                                                'speed_multiplier': {},
                                                'interact_vibrations': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:use_remainder': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:use_remainder': {'type': _C, 'children': {}}
                                    }
                                },
                                'minecraft:weapon': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:weapon': {
                                            'type': _C,
                                            'children': {
                                                'item_damage_per_attack': {},
                                                'disable_blocking_for_seconds': {}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        'abilities': {
            'type': _C,
            'children': {
                'abilities': {
                    'type': _C,
                    'children': {
                        'flying': {'type': _B, 'children': {}},
                        'flySpeed': {'type': _F, 'children': {}},
                        'instabuild': {'type': _B, 'children': {}},
                        'invulnerable': {'type': _B, 'children': {}},
                        'mayBuild': {'type': _B, 'children': {}},
                        'mayfly': {'type': _B, 'children': {}},
                        'walkSpeed': {'type': _F, 'children': {}}
                    }
                },
                'DataVersion': {'type': _I, 'children': {}},
                'Dimension': {'type': _STR, 'children': {}},
                'EnderItems': {
                    'type': _LS,
                    'children': {
                        '[]': {
                            'type': _C,
                            'children': {
                                'Slot': {'type': _B, 'children': {}}
                            }
                        }
                    }
                },
                'entered_nether_pos': {
                    'type': _LS,
                    'children': {
                        '[]': {'type': _D, 'children': {}}
                    }
                },
                'foodExhaustionLevel': {'type': _F, 'children': {}},
                'foodLevel': {'type': _I, 'children': {}},
                'foodSaturationLevel': {'type': _F, 'children': {}},
                'foodTickTimer': {'type': _I, 'children': {}},
                'ignore_fall_damage_from_current_explosion': {'type': _B, 'children': {}},
                'Inventory': {
                    'type': _LS,
                    'children': {
                        '[]': {'type': _C, 'children': {}}
                    }
                },
                'LastDeathLocation': {
                    'type': _C,
                    'children': {
                        'dimension': {'type': _STR, 'children': {}},
                        'pos': {'type': _IA, 'children': {}}
                    }
                },
                'playerGameType': {'type': _I, 'children': {}},
                'previousPlayerGameType': {'type': _I, 'children': {}},
                'recipeBook': {'type': _C, 'children': {}},
                'RootVehicle': {
                    'type': _C,
                    'children': {
                        'Attach': {'type': _IA, 'children': {}},
                        'Entity': {'type': _C, 'children': {}}
                    }
                },
                'Score': {'type': _I, 'children': {}},
                'seenCredits': {'type': _B, 'children': {}},
                'SelectedItem': {'type': _C, 'children': {}},
                'SelectedItemSlot': {'type': _I, 'children': {}},
                'ShoulderEntityLeft': {'type': _C, 'children': {}},
                'ShoulderEntityRight': {'type': _C, 'children': {}},
                'SleepTimer': {'type': _S, 'children': {}},
                'respawn': {
                    'type': _C,
                    'children': {
                        'pos': {'type': _IA, 'children': {}},
                        'yaw': {'type': _F, 'children': {}},
                        'dimension': {'type': _STR, 'children': {}},
                        'pitch': {'type': _F, 'children': {}},
                        'forced': {'type': _B, 'children': {}}
                    }
                },
                'warden_spawn_tracker': {
                    'type': _C,
                    'children': {
                        'warning_level': {'type': _I, 'children': {}},
                        'cooldown_ticks': {'type': _I, 'children': {}},
                        'ticks_since_last_warning': {'type': _I, 'children': {}}
                    }
                },
                'XpLevel': {'type': _I, 'children': {}},
                'XpP': {'type': _F, 'children': {}},
                'XpSeed': {'type': _I, 'children': {}},
                'XpTotal': {'type': _I, 'children': {}}
            }
        },
        'MoreCarrotTicks': {
            'type': _C,
            'children': {
                'MoreCarrotTicks': {'type': _I, 'children': {}},
                'RabbitType': {'type': _I, 'children': {}}
            }
        },
        'AttackTick': {
            'type': _C,
            'children': {
                'AttackTick': {'type': _I, 'children': {}},
                'RoarTick': {'type': _I, 'children': {}},
                'StunTick': {'type': _I, 'children': {}}
            }
        },
        'Color': {
            'type': _C,
            'children': {
                'Color': {'type': _B, 'children': {}},
                'Sheared': {'type': _B, 'children': {}}
            }
        },
        'AttachFace': {
            'type': _C,
            'children': {
                'AttachFace': {'type': _B, 'children': {}},
                'Color': {'type': _B, 'children': {}},
                'Peek': {'type': _B, 'children': {}}
            }
        },
        'StrayConversionTime': {
            'type': _C,
            'children': {
                'StrayConversionTime': {'type': _I, 'children': {}}
            }
        },
        'Pumpkin': {
            'type': _C,
            'children': {
                'Pumpkin': {'type': _B, 'children': {}}
            }
        },
        'pickup_timer': {
            'type': _C,
            'children': {
                'pickup_timer': {'type': _I, 'children': {}},
                'from_bucket': {'type': _B, 'children': {}},
                'fuse': {'type': _I, 'children': {}}
            }
        },
        'Age': {
            'type': _C,
            'children': {
                'Age': {'type': _I, 'children': {}},
                'FromBucket': {'type': _B, 'children': {}},
                'Count': {'type': _I, 'children': {}},
                'Health': {'type': _S, 'children': {}},
                'Value': {'type': _S, 'children': {}},
                'Item': {'type': _C, 'children': {}},
                'Owner': {'type': _IA, 'children': {}},
                'PickupDelay': {'type': _S, 'children': {}},
                'Thrower': {'type': _IA, 'children': {}},
                'Color': {'type': _I, 'children': {}},
                'Duration': {'type': _I, 'children': {}},
                'DurationOnUse': {'type': _I, 'children': {}},
                'potion_contents': {'type': _STR, 'children': {}},
                'custom_particle': {
                    'type': _C,
                    'children': {
                        'type': {'type': _STR, 'children': {}}
                    }
                },
                'potion_duration_scale': {'type': _F, 'children': {}},
                'Radius': {'type': _F, 'children': {}},
                'RadiusOnUse': {'type': _F, 'children': {}},
                'RadiusPerTick': {'type': _F, 'children': {}},
                'ReapplicationDelay': {'type': _I, 'children': {}},
                'WaitTime': {'type': _I, 'children': {}}
            }
        },
        'has_egg': {
            'type': _C,
            'children': {
                'has_egg': {'type': _B, 'children': {}}
            }
        },
        'bound_pos': {
            'type': _C,
            'children': {
                'bound_pos': {'type': _IA, 'children': {}},
                'life_ticks': {'type': _I, 'children': {}},
                'owner': {'type': _IA, 'children': {}}
            }
        },
        'Gossips': {
            'type': _C,
            'children': {
                'Gossips': {
                    'type': _LS,
                    'children': {
                        '[]': {
                            'type': _C,
                            'children': {
                                'Value': {'type': _I, 'children': {}},
                                'Target': {'type': _IA, 'children': {}},
                                'Type': {'type': _STR, 'children': {}}
                            }
                        }
                    }
                },
                'Offers': {
                    'type': _C,
                    'children': {
                        'Recipes': {
                            'type': _LS,
                            'children': {
                                '[]': {
                                    'type': _C,
                                    'children': {
                                        'buy': {'type': _C, 'children': {}},
                                        'buyB': {'type': _C, 'children': {}},
                                        'demand': {'type': _I, 'children': {}},
                                        'maxUses': {'type': _I, 'children': {}},
                                        'priceMultiplier': {'type': _F, 'children': {}},
                                        'rewardExp': {'type': _B, 'children': {}},
                                        'sell': {'type': _C, 'children': {}},
                                        'specialPrice': {'type': _I, 'children': {}},
                                        'uses': {'type': _I, 'children': {}},
                                        'xp': {'type': _I, 'children': {}}
                                    }
                                }
                            }
                        }
                    }
                },
                'VillagerData': {
                    'type': _C,
                    'children': {
                        'level': {'type': _I, 'children': {}},
                        'profession': {'type': _STR, 'children': {}},
                        'type': {'type': _STR, 'children': {}}
                    }
                },
                'Xp': {'type': _I, 'children': {}},
                'Inventory': {
                    'type': _LS,
                    'children': {
                        '[]': {'type': _C, 'children': {}}
                    }
                },
                'LastRestock': {'type': _L, 'children': {}},
                'LastGossipDecay': {'type': _L, 'children': {}},
                'RestocksToday': {'type': _I, 'children': {}},
                'Willing': {'type': _B, 'children': {}},
                'CanBreakDoors': {'type': _B, 'children': {}},
                'DrownedConversionTime': {'type': _I, 'children': {}},
                'InWaterTime': {'type': _I, 'children': {}},
                'IsBaby': {'type': _B, 'children': {}},
                'ConversionTime': {'type': _I, 'children': {}},
                'ConversionPlayer': {'type': _IA, 'children': {}}
            }
        },
        'Johnny': {
            'type': _C,
            'children': {
                'Johnny': {'type': _B, 'children': {}}
            }
        },
        'DespawnDelay': {
            'type': _C,
            'children': {
                'DespawnDelay': {'type': _I, 'children': {}},
                'Offers': {
                    'type': _C,
                    'children': {
                        'Recipes': {
                            'type': _LS,
                            'children': {
                                '[]': {
                                    'type': _C,
                                    'children': {
                                        'buy': {'type': _C, 'children': {}},
                                        'buyB': {'type': _C, 'children': {}},
                                        'maxUses': {'type': _I, 'children': {}},
                                        'rewardExp': {'type': _B, 'children': {}},
                                        'sell': {'type': _C, 'children': {}},
                                        'uses': {'type': _I, 'children': {}}
                                    }
                                }
                            }
                        }
                    }
                },
                'wander_target': {'type': _IA, 'children': {}},
                'Inventory': {
                    'type': _LS,
                    'children': {
                        '[]': {'type': _C, 'children': {}}
                    }
                }
            }
        },
        'anger': {
            'type': _C,
            'children': {
                'anger': {
                    'type': _C,
                    'children': {
                        'suspects': {
                            'type': _LS,
                            'children': {
                                '[]': {
                                    'type': _C,
                                    'children': {
                                        'anger': {'type': _I, 'children': {}},
                                        'uuid': {'type': _IA, 'children': {}}
                                    }
                                }
                            }
                        }
                    }
                },
                'listener': {
                    'type': _C,
                    'children': {
                        'event': {
                            'type': _C,
                            'children': {
                                'distance': {'type': _F, 'children': {}},
                                'game_event': {'type': _STR, 'children': {}},
                                'pos': {
                                    'type': _LS,
                                    'children': {
                                        '[]': {'type': _D, 'children': {}}
                                    }
                                },
                                'projectile_owner': {'type': _IA, 'children': {}},
                                'source': {'type': _IA, 'children': {}}
                            }
                        },
                        'event_delay': {'type': _I, 'children': {}},
                        'selector': {
                            'type': _C,
                            'children': {
                                'tick': {'type': _L, 'children': {}},
                                'event': {'type': _C, 'children': {}}
                            }
                        }
                    }
                }
            }
        },
        'Invul': {
            'type': _C,
            'children': {
                'Invul': {'type': _I, 'children': {}}
            }
        },
        'IsBaby': {
            'type': _C,
            'children': {
                'IsBaby': {'type': _B, 'children': {}}
            }
        },
        'Item': {
            'type': _C,
            'children': {
                'Item': {'type': _C, 'children': {}}
            }
        },
        'FireworksItem': {
            'type': _C,
            'children': {
                'FireworksItem': {'type': _C, 'children': {}},
                'Life': {'type': _I, 'children': {}},
                'LifeTime': {'type': _I, 'children': {}},
                'ShotAtAngle': {'type': _B, 'children': {}}
            }
        },
        'Steps': {
            'type': _C,
            'children': {
                'Steps': {'type': _I, 'children': {}},
                'Target': {'type': _IA, 'children': {}},
                'TXD': {'type': _D, 'children': {}},
                'TYD': {'type': _D, 'children': {}},
                'TZD': {'type': _D, 'children': {}}
            }
        },
        'Duration': {
            'type': _C,
            'children': {
                'Duration': {'type': _I, 'children': {}}
            }
        },
        'DealtDamage': {
            'type': _C,
            'children': {
                'DealtDamage': {'type': _B, 'children': {}}
            }
        },
        'dangerous': {
            'type': _C,
            'children': {
                'dangerous': {'type': _B, 'children': {}}
            }
        },
        'Command': {
            'type': _C,
            'children': {
                'Command': {'type': _STR, 'children': {}},
                'LastOutput': {'type': _STR, 'children': {}},
                'SuccessCount': {'type': _I, 'children': {}},
                'TrackOutput': {'type': _B, 'children': {}}
            }
        },
        'Fuel': {
            'type': _C,
            'children': {
                'Fuel': {'type': _S, 'children': {}},
                'PushX': {'type': _D, 'children': {}},
                'PushZ': {'type': _D, 'children': {}}
            }
        },
        'Enabled': {
            'type': _C,
            'children': {
                'Enabled': {'type': _B, 'children': {}}
            }
        },
        'Delay': {
            'type': _C,
            'children': {
                'Delay': {'type': _S, 'children': {}},
                'MaxNearbyEntities': {'type': _S, 'children': {}},
                'MaxSpawnDelay': {'type': _S, 'children': {}},
                'MinSpawnDelay': {'type': _S, 'children': {}},
                'RequiredPlayerRange': {'type': _S, 'children': {}},
                'SpawnCount': {'type': _S, 'children': {}},
                'SpawnData': {'type': _C, 'children': {}},
                'SpawnPotentials': {
                    'type': _LS,
                    'children': {
                        '[]': {
                            'type': _C,
                            'children': {
                                'weight': {'type': _I, 'children': {}},
                                'data': {'type': _C, 'children': {}}
                            }
                        }
                    }
                },
                'SpawnRange': {'type': _S, 'children': {}}
            }
        },
        'fuse': {
            'type': _C,
            'children': {
                'fuse': {'type': _S, 'children': {}},
                'explosion_power': {'type': _F, 'children': {}},
                'explosion_speed_factor': {'type': _F, 'children': {}},
                'block_state': {
                    'type': _C,
                    'children': {
                        'Name': {'type': _STR, 'children': {}},
                        'Properties': {
                            'type': _C,
                            'children': {
                                'Name': {'type': _STR, 'children': {}}
                            }
                        }
                    }
                },
                'owner': {'type': _IA, 'children': {}}
            }
        },
        'BlockState': {
            'type': _C,
            'children': {
                'BlockState': {'type': _C, 'children': {}},
                'TileEntityData': {'type': _C, 'children': {}},
                'CancelDrop': {'type': _B, 'children': {}},
                'DropItem': {'type': _B, 'children': {}},
                'FallHurtAmount': {'type': _F, 'children': {}},
                'FallHurtMax': {'type': _I, 'children': {}},
                'HurtEntities': {'type': _B, 'children': {}},
                'Time': {'type': _I, 'children': {}}
            }
        },
        'block_state': {
            'type': _C,
            'children': {
                'block_state': {'type': _C, 'children': {}}
            }
        },
        'item': {
            'type': _C,
            'children': {
                'item': {'type': _C, 'children': {}},
                'item_display': {'type': _STR, 'children': {}},
                'spawn_item_after_ticks': {'type': _L, 'children': {}}
            }
        },
        'alignment': {
            'type': _C,
            'children': {
                'alignment': {'type': _STR, 'children': {}},
                'background': {'type': _I, 'children': {}},
                'default_background': {'type': _B, 'children': {}},
                'line_width': {'type': _I, 'children': {}},
                'see_through': {'type': _B, 'children': {}},
                'shadow': {'type': _B, 'children': {}},
                'text': {'type': _STR, 'children': {}},
                'text_opacity': {'type': _B, 'children': {}}
            }
        },
        'beam_target': {
            'type': _C,
            'children': {
                'beam_target': {'type': _IA, 'children': {}},
                'ShowBottom': {'type': _B, 'children': {}}
            }
        },
        'Owner': {
            'type': _C,
            'children': {
                'Owner': {'type': _IA, 'children': {}},
                'Warmup': {'type': _I, 'children': {}}
            }
        },
        'Fixed': {
            'type': _C,
            'children': {
                'Fixed': {'type': _B, 'children': {}},
                'Invisible': {'type': _B, 'children': {}},
                'Item': {'type': _C, 'children': {}},
                'ItemDropChance': {'type': _F, 'children': {}},
                'ItemRotation': {'type': _B, 'children': {}}
            }
        },
        'width': {
            'type': _C,
            'children': {
                'width': {'type': _F, 'children': {}},
                'height': {'type': _F, 'children': {}},
                'response': {'type': _B, 'children': {}},
                'attack': {
                    'type': _C,
                    'children': {
                        'player': {'type': _IA, 'children': {}},
                        'timestamp': {'type': _L, 'children': {}}
                    }
                },
                'interaction': {
                    'type': _C,
                    'children': {
                        'player': {'type': _IA, 'children': {}},
                        'timestamp': {'type': _L, 'children': {}}
                    }
                }
            }
        },
        'facing': {
            'type': _C,
            'children': {
                'facing': {'type': _B, 'children': {}},
                'variant': {'type': _STR, 'children': {}}
            }
        },
        'Pos': {
            'type': _LS,
            'children': {
                '[]': {'type': _D, 'children': {}}
            }
        },
        'Motion': {
            'type': _LS,
            'children': {
                '[]': {'type': _D, 'children': {}}
            }
        },
        'Rotation': {
            'type': _LS,
            'children': {
                '[]': {'type': _F, 'children': {}}
            }
        },
        'HandItems': {
            'type': _LS,
            'children': {
                '[]': {
                    'type': _C,
                    'children': {
                        'id': {'type': _STR, 'children': {}},
                        'Count': {'type': _B, 'children': {}},
                        'Slot': {'type': _B, 'children': {}},
                        'tag': {'type': _C, 'children': {}},
                        'components': {
                            'type': _C,
                            'children': {
                                'id': {
                                    'type': _STR,
                                    'children': {
                                        'id': {'type': _STR, 'children': {}},
                                        'keepPacked': {'type': _B, 'children': {}},
                                        'x': {'type': _I, 'children': {}},
                                        'y': {'type': _I, 'children': {}},
                                        'z': {'type': _I, 'children': {}},
                                        'components': {'type': _C, 'children': {}}
                                    }
                                },
                                'components': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:follow': {'type': _B, 'children': {}}
                                    }
                                },
                                'minecraft:attack_range': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:attack_range': {
                                            'type': _C,
                                            'children': {
                                                'min_reach': {},
                                                'max_reach': {},
                                                'min_creative_reach': {},
                                                'max_creative_reach': {},
                                                'hitbox_margin': {},
                                                'mob_factor': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:attribute_modifiers': {
                                    'type': _LS,
                                    'children': {
                                        '[]': {
                                            'type': _LS,
                                            'children': {
                                                '[]': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:block_entity_data': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:block_entity_data': {'type': _C, 'children': {}}
                                    }
                                },
                                'minecraft:blocks_attacks': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:blocks_attacks': {
                                            'type': _C,
                                            'children': {
                                                'block_delay_seconds': {},
                                                'disable_cooldown_scale': {},
                                                'damage_reductions': {},
                                                'item_damage': {},
                                                'block_sound': {},
                                                'disabled_sound': {},
                                                'bypassed_by': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:break_sound': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:break_sound': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:bucket_entity_data': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:bucket_entity_data': {
                                            'type': _C,
                                            'children': {
                                                'NoAI': {},
                                                'Silent': {},
                                                'NoGravity': {},
                                                'Glowing': {},
                                                'Invulnerable': {},
                                                'AgeLocked': {},
                                                'Health': {},
                                                'Age': {},
                                                'HuntingCooldown': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:can_break': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:can_break': {
                                            'type': _C,
                                            'children': {
                                                'blocks': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:can_place_on': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:can_place_on': {
                                            'type': _C,
                                            'children': {
                                                'blocks': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:consumable': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:consumable': {
                                            'type': _C,
                                            'children': {
                                                'consume_seconds': {},
                                                'animation': {},
                                                'sound': {},
                                                'has_consume_particles': {},
                                                'on_consume_effects': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:custom_model_data': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:custom_model_data': {
                                            'type': _C,
                                            'children': {
                                                'floats': {},
                                                'flags': {},
                                                'strings': {},
                                                'colors': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:custom_name': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:custom_name': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:damage_resistant': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:damage_resistant': {
                                            'type': _C,
                                            'children': {
                                                'types': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:damage_type': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:damage_type': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:death_protection': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:death_protection': {
                                            'type': _C,
                                            'children': {
                                                'death_effects': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:enchantable': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:enchantable': {
                                            'type': _C,
                                            'children': {
                                                'value': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:enchantments': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:enchantments': {
                                            'type': _C,
                                            'children': {
                                                '<enchantment ID>': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:equippable': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:equippable': {
                                            'type': _C,
                                            'children': {
                                                'slot': {},
                                                'equip_sound': {},
                                                'asset_id': {},
                                                'allowed_entities': {},
                                                'dispensable': {},
                                                'swappable': {},
                                                'damage_on_hurt': {},
                                                'equip_on_interact': {},
                                                'camera_overlay': {},
                                                'can_be_sheared': {},
                                                'shearing_sound': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:glider': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:glider': {'type': _C, 'children': {}}
                                    }
                                },
                                'minecraft:instrument': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:instrument': {
                                            'type': _STR,
                                            'children': {
                                                'description': {},
                                                'sound_event': {},
                                                'use_duration': {},
                                                'range': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:item_model': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:item_model': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:item_name': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:item_name': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:jukebox_playable': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:jukebox_playable': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:kinetic_weapon': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:kinetic_weapon': {
                                            'type': _C,
                                            'children': {
                                                'delay_ticks': {},
                                                'damage_conditions': {},
                                                'dismount_conditions': {},
                                                'knockback_conditions': {},
                                                'forward_movement': {},
                                                'damage_multiplier': {},
                                                'sound': {},
                                                'hit_sound': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:max_damage': {
                                    'type': _I,
                                    'children': {
                                        'minecraft:max_damage': {'type': _I, 'children': {}}
                                    }
                                },
                                'minecraft:minimum_attack_charge': {
                                    'type': _F,
                                    'children': {
                                        'minecraft:minimum_attack_charge': {'type': _F, 'children': {}}
                                    }
                                },
                                'minecraft:piercing_weapon': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:piercing_weapon': {
                                            'type': _C,
                                            'children': {
                                                'deals_knockback': {},
                                                'dismounts': {},
                                                'sound': {},
                                                'hit_sound': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:potion_contents': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:potion_contents': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:potion_duration_scale': {
                                    'type': _F,
                                    'children': {
                                        'minecraft:potion_duration_scale': {'type': _F, 'children': {}}
                                    }
                                },
                                'minecraft:profile': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:profile': {'type': _STR, 'children': {}},
                                        'name': {
                                            'type': _STR,
                                            'children': {
                                                'name': {},
                                                'id': {},
                                                'properties': {},
                                                'texture': {},
                                                'cape': {},
                                                'elytra': {},
                                                'model': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:provides_banner_patterns': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:provides_banner_patterns': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:provides_trim_material': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:provides_trim_material': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:repairable': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:repairable': {
                                            'type': _C,
                                            'children': {
                                                'items': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:stored_enchantments': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:stored_enchantments': {
                                            'type': _C,
                                            'children': {
                                                '<enchantment ID>': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:swing_animation': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:swing_animation': {
                                            'type': _C,
                                            'children': {
                                                'type': {},
                                                'duration': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:tooltip_display': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:tooltip_display': {
                                            'type': _C,
                                            'children': {
                                                'hide_tooltip': {},
                                                'hidden_components': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:tooltip_style': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:tooltip_style': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:use_cooldown': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:use_cooldown': {
                                            'type': _C,
                                            'children': {
                                                'seconds': {},
                                                'cooldown_group': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:use_effects': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:use_effects': {
                                            'type': _C,
                                            'children': {
                                                'can_sprint': {},
                                                'speed_multiplier': {},
                                                'interact_vibrations': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:use_remainder': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:use_remainder': {'type': _C, 'children': {}}
                                    }
                                },
                                'minecraft:weapon': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:weapon': {
                                            'type': _C,
                                            'children': {
                                                'item_damage_per_attack': {},
                                                'disable_blocking_for_seconds': {}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        'ArmorItems': {
            'type': _LS,
            'children': {
                '[]': {
                    'type': _C,
                    'children': {
                        'id': {'type': _STR, 'children': {}},
                        'Count': {'type': _B, 'children': {}},
                        'Slot': {'type': _B, 'children': {}},
                        'tag': {'type': _C, 'children': {}},
                        'components': {
                            'type': _C,
                            'children': {
                                'id': {
                                    'type': _STR,
                                    'children': {
                                        'id': {'type': _STR, 'children': {}},
                                        'keepPacked': {'type': _B, 'children': {}},
                                        'x': {'type': _I, 'children': {}},
                                        'y': {'type': _I, 'children': {}},
                                        'z': {'type': _I, 'children': {}},
                                        'components': {'type': _C, 'children': {}}
                                    }
                                },
                                'components': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:follow': {'type': _B, 'children': {}}
                                    }
                                },
                                'minecraft:attack_range': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:attack_range': {
                                            'type': _C,
                                            'children': {
                                                'min_reach': {},
                                                'max_reach': {},
                                                'min_creative_reach': {},
                                                'max_creative_reach': {},
                                                'hitbox_margin': {},
                                                'mob_factor': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:attribute_modifiers': {
                                    'type': _LS,
                                    'children': {
                                        '[]': {
                                            'type': _LS,
                                            'children': {
                                                '[]': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:block_entity_data': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:block_entity_data': {'type': _C, 'children': {}}
                                    }
                                },
                                'minecraft:blocks_attacks': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:blocks_attacks': {
                                            'type': _C,
                                            'children': {
                                                'block_delay_seconds': {},
                                                'disable_cooldown_scale': {},
                                                'damage_reductions': {},
                                                'item_damage': {},
                                                'block_sound': {},
                                                'disabled_sound': {},
                                                'bypassed_by': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:break_sound': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:break_sound': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:bucket_entity_data': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:bucket_entity_data': {
                                            'type': _C,
                                            'children': {
                                                'NoAI': {},
                                                'Silent': {},
                                                'NoGravity': {},
                                                'Glowing': {},
                                                'Invulnerable': {},
                                                'AgeLocked': {},
                                                'Health': {},
                                                'Age': {},
                                                'HuntingCooldown': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:can_break': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:can_break': {
                                            'type': _C,
                                            'children': {
                                                'blocks': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:can_place_on': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:can_place_on': {
                                            'type': _C,
                                            'children': {
                                                'blocks': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:consumable': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:consumable': {
                                            'type': _C,
                                            'children': {
                                                'consume_seconds': {},
                                                'animation': {},
                                                'sound': {},
                                                'has_consume_particles': {},
                                                'on_consume_effects': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:custom_model_data': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:custom_model_data': {
                                            'type': _C,
                                            'children': {
                                                'floats': {},
                                                'flags': {},
                                                'strings': {},
                                                'colors': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:custom_name': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:custom_name': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:damage_resistant': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:damage_resistant': {
                                            'type': _C,
                                            'children': {
                                                'types': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:damage_type': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:damage_type': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:death_protection': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:death_protection': {
                                            'type': _C,
                                            'children': {
                                                'death_effects': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:enchantable': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:enchantable': {
                                            'type': _C,
                                            'children': {
                                                'value': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:enchantments': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:enchantments': {
                                            'type': _C,
                                            'children': {
                                                '<enchantment ID>': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:equippable': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:equippable': {
                                            'type': _C,
                                            'children': {
                                                'slot': {},
                                                'equip_sound': {},
                                                'asset_id': {},
                                                'allowed_entities': {},
                                                'dispensable': {},
                                                'swappable': {},
                                                'damage_on_hurt': {},
                                                'equip_on_interact': {},
                                                'camera_overlay': {},
                                                'can_be_sheared': {},
                                                'shearing_sound': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:glider': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:glider': {'type': _C, 'children': {}}
                                    }
                                },
                                'minecraft:instrument': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:instrument': {
                                            'type': _STR,
                                            'children': {
                                                'description': {},
                                                'sound_event': {},
                                                'use_duration': {},
                                                'range': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:item_model': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:item_model': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:item_name': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:item_name': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:jukebox_playable': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:jukebox_playable': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:kinetic_weapon': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:kinetic_weapon': {
                                            'type': _C,
                                            'children': {
                                                'delay_ticks': {},
                                                'damage_conditions': {},
                                                'dismount_conditions': {},
                                                'knockback_conditions': {},
                                                'forward_movement': {},
                                                'damage_multiplier': {},
                                                'sound': {},
                                                'hit_sound': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:max_damage': {
                                    'type': _I,
                                    'children': {
                                        'minecraft:max_damage': {'type': _I, 'children': {}}
                                    }
                                },
                                'minecraft:minimum_attack_charge': {
                                    'type': _F,
                                    'children': {
                                        'minecraft:minimum_attack_charge': {'type': _F, 'children': {}}
                                    }
                                },
                                'minecraft:piercing_weapon': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:piercing_weapon': {
                                            'type': _C,
                                            'children': {
                                                'deals_knockback': {},
                                                'dismounts': {},
                                                'sound': {},
                                                'hit_sound': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:potion_contents': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:potion_contents': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:potion_duration_scale': {
                                    'type': _F,
                                    'children': {
                                        'minecraft:potion_duration_scale': {'type': _F, 'children': {}}
                                    }
                                },
                                'minecraft:profile': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:profile': {'type': _STR, 'children': {}},
                                        'name': {
                                            'type': _STR,
                                            'children': {
                                                'name': {},
                                                'id': {},
                                                'properties': {},
                                                'texture': {},
                                                'cape': {},
                                                'elytra': {},
                                                'model': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:provides_banner_patterns': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:provides_banner_patterns': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:provides_trim_material': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:provides_trim_material': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:repairable': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:repairable': {
                                            'type': _C,
                                            'children': {
                                                'items': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:stored_enchantments': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:stored_enchantments': {
                                            'type': _C,
                                            'children': {
                                                '<enchantment ID>': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:swing_animation': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:swing_animation': {
                                            'type': _C,
                                            'children': {
                                                'type': {},
                                                'duration': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:tooltip_display': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:tooltip_display': {
                                            'type': _C,
                                            'children': {
                                                'hide_tooltip': {},
                                                'hidden_components': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:tooltip_style': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:tooltip_style': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:use_cooldown': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:use_cooldown': {
                                            'type': _C,
                                            'children': {
                                                'seconds': {},
                                                'cooldown_group': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:use_effects': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:use_effects': {
                                            'type': _C,
                                            'children': {
                                                'can_sprint': {},
                                                'speed_multiplier': {},
                                                'interact_vibrations': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:use_remainder': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:use_remainder': {'type': _C, 'children': {}}
                                    }
                                },
                                'minecraft:weapon': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:weapon': {
                                            'type': _C,
                                            'children': {
                                                'item_damage_per_attack': {},
                                                'disable_blocking_for_seconds': {}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        'EnderItems': {
            'type': _LS,
            'children': {
                '[]': {
                    'type': _C,
                    'children': {
                        'id': {'type': _STR, 'children': {}},
                        'Count': {'type': _B, 'children': {}},
                        'Slot': {'type': _B, 'children': {}},
                        'tag': {'type': _C, 'children': {}},
                        'components': {
                            'type': _C,
                            'children': {
                                'id': {
                                    'type': _STR,
                                    'children': {
                                        'id': {'type': _STR, 'children': {}},
                                        'keepPacked': {'type': _B, 'children': {}},
                                        'x': {'type': _I, 'children': {}},
                                        'y': {'type': _I, 'children': {}},
                                        'z': {'type': _I, 'children': {}},
                                        'components': {'type': _C, 'children': {}}
                                    }
                                },
                                'components': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:follow': {'type': _B, 'children': {}}
                                    }
                                },
                                'minecraft:attack_range': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:attack_range': {
                                            'type': _C,
                                            'children': {
                                                'min_reach': {},
                                                'max_reach': {},
                                                'min_creative_reach': {},
                                                'max_creative_reach': {},
                                                'hitbox_margin': {},
                                                'mob_factor': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:attribute_modifiers': {
                                    'type': _LS,
                                    'children': {
                                        '[]': {
                                            'type': _LS,
                                            'children': {
                                                '[]': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:block_entity_data': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:block_entity_data': {'type': _C, 'children': {}}
                                    }
                                },
                                'minecraft:blocks_attacks': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:blocks_attacks': {
                                            'type': _C,
                                            'children': {
                                                'block_delay_seconds': {},
                                                'disable_cooldown_scale': {},
                                                'damage_reductions': {},
                                                'item_damage': {},
                                                'block_sound': {},
                                                'disabled_sound': {},
                                                'bypassed_by': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:break_sound': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:break_sound': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:bucket_entity_data': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:bucket_entity_data': {
                                            'type': _C,
                                            'children': {
                                                'NoAI': {},
                                                'Silent': {},
                                                'NoGravity': {},
                                                'Glowing': {},
                                                'Invulnerable': {},
                                                'AgeLocked': {},
                                                'Health': {},
                                                'Age': {},
                                                'HuntingCooldown': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:can_break': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:can_break': {
                                            'type': _C,
                                            'children': {
                                                'blocks': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:can_place_on': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:can_place_on': {
                                            'type': _C,
                                            'children': {
                                                'blocks': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:consumable': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:consumable': {
                                            'type': _C,
                                            'children': {
                                                'consume_seconds': {},
                                                'animation': {},
                                                'sound': {},
                                                'has_consume_particles': {},
                                                'on_consume_effects': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:custom_model_data': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:custom_model_data': {
                                            'type': _C,
                                            'children': {
                                                'floats': {},
                                                'flags': {},
                                                'strings': {},
                                                'colors': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:custom_name': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:custom_name': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:damage_resistant': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:damage_resistant': {
                                            'type': _C,
                                            'children': {
                                                'types': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:damage_type': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:damage_type': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:death_protection': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:death_protection': {
                                            'type': _C,
                                            'children': {
                                                'death_effects': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:enchantable': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:enchantable': {
                                            'type': _C,
                                            'children': {
                                                'value': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:enchantments': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:enchantments': {
                                            'type': _C,
                                            'children': {
                                                '<enchantment ID>': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:equippable': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:equippable': {
                                            'type': _C,
                                            'children': {
                                                'slot': {},
                                                'equip_sound': {},
                                                'asset_id': {},
                                                'allowed_entities': {},
                                                'dispensable': {},
                                                'swappable': {},
                                                'damage_on_hurt': {},
                                                'equip_on_interact': {},
                                                'camera_overlay': {},
                                                'can_be_sheared': {},
                                                'shearing_sound': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:glider': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:glider': {'type': _C, 'children': {}}
                                    }
                                },
                                'minecraft:instrument': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:instrument': {
                                            'type': _STR,
                                            'children': {
                                                'description': {},
                                                'sound_event': {},
                                                'use_duration': {},
                                                'range': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:item_model': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:item_model': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:item_name': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:item_name': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:jukebox_playable': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:jukebox_playable': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:kinetic_weapon': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:kinetic_weapon': {
                                            'type': _C,
                                            'children': {
                                                'delay_ticks': {},
                                                'damage_conditions': {},
                                                'dismount_conditions': {},
                                                'knockback_conditions': {},
                                                'forward_movement': {},
                                                'damage_multiplier': {},
                                                'sound': {},
                                                'hit_sound': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:max_damage': {
                                    'type': _I,
                                    'children': {
                                        'minecraft:max_damage': {'type': _I, 'children': {}}
                                    }
                                },
                                'minecraft:minimum_attack_charge': {
                                    'type': _F,
                                    'children': {
                                        'minecraft:minimum_attack_charge': {'type': _F, 'children': {}}
                                    }
                                },
                                'minecraft:piercing_weapon': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:piercing_weapon': {
                                            'type': _C,
                                            'children': {
                                                'deals_knockback': {},
                                                'dismounts': {},
                                                'sound': {},
                                                'hit_sound': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:potion_contents': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:potion_contents': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:potion_duration_scale': {
                                    'type': _F,
                                    'children': {
                                        'minecraft:potion_duration_scale': {'type': _F, 'children': {}}
                                    }
                                },
                                'minecraft:profile': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:profile': {'type': _STR, 'children': {}},
                                        'name': {
                                            'type': _STR,
                                            'children': {
                                                'name': {},
                                                'id': {},
                                                'properties': {},
                                                'texture': {},
                                                'cape': {},
                                                'elytra': {},
                                                'model': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:provides_banner_patterns': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:provides_banner_patterns': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:provides_trim_material': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:provides_trim_material': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:repairable': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:repairable': {
                                            'type': _C,
                                            'children': {
                                                'items': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:stored_enchantments': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:stored_enchantments': {
                                            'type': _C,
                                            'children': {
                                                '<enchantment ID>': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:swing_animation': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:swing_animation': {
                                            'type': _C,
                                            'children': {
                                                'type': {},
                                                'duration': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:tooltip_display': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:tooltip_display': {
                                            'type': _C,
                                            'children': {
                                                'hide_tooltip': {},
                                                'hidden_components': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:tooltip_style': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:tooltip_style': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:use_cooldown': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:use_cooldown': {
                                            'type': _C,
                                            'children': {
                                                'seconds': {},
                                                'cooldown_group': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:use_effects': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:use_effects': {
                                            'type': _C,
                                            'children': {
                                                'can_sprint': {},
                                                'speed_multiplier': {},
                                                'interact_vibrations': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:use_remainder': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:use_remainder': {'type': _C, 'children': {}}
                                    }
                                },
                                'minecraft:weapon': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:weapon': {
                                            'type': _C,
                                            'children': {
                                                'item_damage_per_attack': {},
                                                'disable_blocking_for_seconds': {}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        'Items': {
            'type': _LS,
            'children': {
                '[]': {
                    'type': _C,
                    'children': {
                        'id': {'type': _STR, 'children': {}},
                        'Count': {'type': _B, 'children': {}},
                        'Slot': {'type': _B, 'children': {}},
                        'tag': {'type': _C, 'children': {}},
                        'components': {
                            'type': _C,
                            'children': {
                                'id': {
                                    'type': _STR,
                                    'children': {
                                        'id': {'type': _STR, 'children': {}},
                                        'keepPacked': {'type': _B, 'children': {}},
                                        'x': {'type': _I, 'children': {}},
                                        'y': {'type': _I, 'children': {}},
                                        'z': {'type': _I, 'children': {}},
                                        'components': {'type': _C, 'children': {}}
                                    }
                                },
                                'components': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:follow': {'type': _B, 'children': {}}
                                    }
                                },
                                'minecraft:attack_range': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:attack_range': {
                                            'type': _C,
                                            'children': {
                                                'min_reach': {},
                                                'max_reach': {},
                                                'min_creative_reach': {},
                                                'max_creative_reach': {},
                                                'hitbox_margin': {},
                                                'mob_factor': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:attribute_modifiers': {
                                    'type': _LS,
                                    'children': {
                                        '[]': {
                                            'type': _LS,
                                            'children': {
                                                '[]': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:block_entity_data': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:block_entity_data': {'type': _C, 'children': {}}
                                    }
                                },
                                'minecraft:blocks_attacks': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:blocks_attacks': {
                                            'type': _C,
                                            'children': {
                                                'block_delay_seconds': {},
                                                'disable_cooldown_scale': {},
                                                'damage_reductions': {},
                                                'item_damage': {},
                                                'block_sound': {},
                                                'disabled_sound': {},
                                                'bypassed_by': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:break_sound': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:break_sound': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:bucket_entity_data': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:bucket_entity_data': {
                                            'type': _C,
                                            'children': {
                                                'NoAI': {},
                                                'Silent': {},
                                                'NoGravity': {},
                                                'Glowing': {},
                                                'Invulnerable': {},
                                                'AgeLocked': {},
                                                'Health': {},
                                                'Age': {},
                                                'HuntingCooldown': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:can_break': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:can_break': {
                                            'type': _C,
                                            'children': {
                                                'blocks': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:can_place_on': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:can_place_on': {
                                            'type': _C,
                                            'children': {
                                                'blocks': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:consumable': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:consumable': {
                                            'type': _C,
                                            'children': {
                                                'consume_seconds': {},
                                                'animation': {},
                                                'sound': {},
                                                'has_consume_particles': {},
                                                'on_consume_effects': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:custom_model_data': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:custom_model_data': {
                                            'type': _C,
                                            'children': {
                                                'floats': {},
                                                'flags': {},
                                                'strings': {},
                                                'colors': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:custom_name': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:custom_name': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:damage_resistant': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:damage_resistant': {
                                            'type': _C,
                                            'children': {
                                                'types': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:damage_type': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:damage_type': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:death_protection': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:death_protection': {
                                            'type': _C,
                                            'children': {
                                                'death_effects': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:enchantable': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:enchantable': {
                                            'type': _C,
                                            'children': {
                                                'value': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:enchantments': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:enchantments': {
                                            'type': _C,
                                            'children': {
                                                '<enchantment ID>': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:equippable': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:equippable': {
                                            'type': _C,
                                            'children': {
                                                'slot': {},
                                                'equip_sound': {},
                                                'asset_id': {},
                                                'allowed_entities': {},
                                                'dispensable': {},
                                                'swappable': {},
                                                'damage_on_hurt': {},
                                                'equip_on_interact': {},
                                                'camera_overlay': {},
                                                'can_be_sheared': {},
                                                'shearing_sound': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:glider': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:glider': {'type': _C, 'children': {}}
                                    }
                                },
                                'minecraft:instrument': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:instrument': {
                                            'type': _STR,
                                            'children': {
                                                'description': {},
                                                'sound_event': {},
                                                'use_duration': {},
                                                'range': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:item_model': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:item_model': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:item_name': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:item_name': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:jukebox_playable': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:jukebox_playable': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:kinetic_weapon': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:kinetic_weapon': {
                                            'type': _C,
                                            'children': {
                                                'delay_ticks': {},
                                                'damage_conditions': {},
                                                'dismount_conditions': {},
                                                'knockback_conditions': {},
                                                'forward_movement': {},
                                                'damage_multiplier': {},
                                                'sound': {},
                                                'hit_sound': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:max_damage': {
                                    'type': _I,
                                    'children': {
                                        'minecraft:max_damage': {'type': _I, 'children': {}}
                                    }
                                },
                                'minecraft:minimum_attack_charge': {
                                    'type': _F,
                                    'children': {
                                        'minecraft:minimum_attack_charge': {'type': _F, 'children': {}}
                                    }
                                },
                                'minecraft:piercing_weapon': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:piercing_weapon': {
                                            'type': _C,
                                            'children': {
                                                'deals_knockback': {},
                                                'dismounts': {},
                                                'sound': {},
                                                'hit_sound': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:potion_contents': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:potion_contents': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:potion_duration_scale': {
                                    'type': _F,
                                    'children': {
                                        'minecraft:potion_duration_scale': {'type': _F, 'children': {}}
                                    }
                                },
                                'minecraft:profile': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:profile': {'type': _STR, 'children': {}},
                                        'name': {
                                            'type': _STR,
                                            'children': {
                                                'name': {},
                                                'id': {},
                                                'properties': {},
                                                'texture': {},
                                                'cape': {},
                                                'elytra': {},
                                                'model': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:provides_banner_patterns': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:provides_banner_patterns': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:provides_trim_material': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:provides_trim_material': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:repairable': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:repairable': {
                                            'type': _C,
                                            'children': {
                                                'items': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:stored_enchantments': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:stored_enchantments': {
                                            'type': _C,
                                            'children': {
                                                '<enchantment ID>': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:swing_animation': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:swing_animation': {
                                            'type': _C,
                                            'children': {
                                                'type': {},
                                                'duration': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:tooltip_display': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:tooltip_display': {
                                            'type': _C,
                                            'children': {
                                                'hide_tooltip': {},
                                                'hidden_components': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:tooltip_style': {
                                    'type': _STR,
                                    'children': {
                                        'minecraft:tooltip_style': {'type': _STR, 'children': {}}
                                    }
                                },
                                'minecraft:use_cooldown': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:use_cooldown': {
                                            'type': _C,
                                            'children': {
                                                'seconds': {},
                                                'cooldown_group': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:use_effects': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:use_effects': {
                                            'type': _C,
                                            'children': {
                                                'can_sprint': {},
                                                'speed_multiplier': {},
                                                'interact_vibrations': {}
                                            }
                                        }
                                    }
                                },
                                'minecraft:use_remainder': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:use_remainder': {'type': _C, 'children': {}}
                                    }
                                },
                                'minecraft:weapon': {
                                    'type': _C,
                                    'children': {
                                        'minecraft:weapon': {
                                            'type': _C,
                                            'children': {
                                                'item_damage_per_attack': {},
                                                'disable_blocking_for_seconds': {}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

if 'Passengers' in ENTITY_SCHEMA['children']:
    ENTITY_SCHEMA['children']['Passengers']['children']['[]'] = ENTITY_SCHEMA