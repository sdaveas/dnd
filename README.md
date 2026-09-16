# D&D Battle Simulation — Layn

This repository contains the complete rules, character data, inventory, companion data, and combat conventions needed to simulate battles involving **Laynlindr Freth (Layn)**.

## Scope

This repository intentionally contains **no campaign history or narrative state**. It focuses on battle simulation.

The intended separation is:

- `characters/` — Layn's persistent character data.
- `companions/` — Baba and companion-specific mechanics.
- `rules/` — generic combat and rules mechanics required by the simulator.

## Authority and rule layers

When resolving a battle, use the following precedence:

1. Explicit current character-sheet values.
2. Explicit campaign/homebrew mechanics recorded in these files.
3. The 2024 D&D rules as represented by the character sheet.
4. Player tactical preferences are **decision policy**, not mechanics.

If a rule is uncertain or a document conflicts with another source, flag the ambiguity rather than silently inventing a mechanic.

## Current character

**Laynlindr Freth (Layn)**  
Dark Elf Rogue — Soulknife — Level 7  
2024 rules

## Character files

- [Character](characters/laynlindr-freth/character.md)
- [Abilities & Features](characters/laynlindr-freth/abilities.md)
- [Skills & Proficiencies](characters/laynlindr-freth/skills.md)
- [Inventory](characters/laynlindr-freth/inventory.md)
- [Combat Profile](characters/laynlindr-freth/combat.md)
- [Baba](companions/baba.md)

## Rules

- [Combat](rules/combat.md)
- [Attacks & Damage](rules/attacks.md)
- [Conditions & States](rules/conditions.md)
- [Mechanics](rules/mechanics.md)

## Simulator goal

Given these definitions plus an encounter state, the simulator should be able to determine legal actions, attack/save modifiers, advantage/disadvantage, damage, reactions, movement, resources, conditions, companion positioning, and the resulting battle state.
